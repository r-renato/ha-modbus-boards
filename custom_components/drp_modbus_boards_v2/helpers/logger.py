# helpers/prefixed_logger.py

from __future__ import annotations

import logging
import sys

class PrefixedLogger:
    """
    Logger helper che premette al messaggio il chiamante reale:
    - '[Classe.metodo] ' se chiamato da un metodo di istanza/classe
    - '[modulo.funzione] ' altrimenti

    Implementa una risalita dello stack "robusta": salta automaticamente
    i frame interni al modulo helper e si ferma al primo frame "esterno".
    """

    # Nomi dei metodi/helper interni da saltare durante la risalita
    _HELPER_FUNCS = {
        "log_debug",
        "log_info",
        "log_warning",
        "log_error",      
        "log_exception", 
        "_qualname_from_frame",
        "caller_qualname_auto",
    }

    @staticmethod
    def _qualname_from_frame(f) -> str:
        """Costruisce il nome qualificato a partire da un frame."""
        if f is None:
            return "<unknown>"

        fn = f.f_code.co_name
        loc = f.f_locals

        # Metodo di istanza / classe
        if "self" in loc:
            return f"{type(loc['self']).__qualname__}.{fn}"
        if "cls" in loc:
            return f"{loc['cls'].__qualname__}.{fn}"

        # Funzione libera: modulo.funzione
        modname = f.f_globals.get("__name__", "")
        return f"{modname}.{fn}" if modname else fn

    @staticmethod
    def caller_qualname_auto() -> str:
        """
        Risale lo stack partendo dal frame del wrapper (log_*)
        finché esce dal modulo helper o dalla catena di helper.

        0 = this (caller_qualname_auto)
        1 = log_* wrapper
        2+ = potenziali frame helper / chiamante reale
        """
        # 1 = il frame di log_* (il nostro wrapper)
        f = sys._getframe(1)
        helper_modname = __name__

        while f:
            modname = f.f_globals.get("__name__", "")
            fn = f.f_code.co_name
            # Esci quando:
            # - il frame NON appartiene più al modulo helper, oppure
            # - è nel modulo helper ma NON è uno degli helper interni
            if modname != helper_modname or fn not in PrefixedLogger._HELPER_FUNCS:
                return PrefixedLogger._qualname_from_frame(f)
            f = f.f_back

        return "<unknown>"

    @staticmethod
    def log_debug(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
        """
        Log DEBUG con prefisso del chiamante reale e stacklevel corretto.
        Uso: PrefixedLogger.log_debug(_LOGGER, "Hello %s", who)
        """
        if not logger.isEnabledFor(logging.DEBUG):
            return

        prefix = f"[{PrefixedLogger.caller_qualname_auto()}] "
        # stacklevel=2 salta il wrapper log_debug per posizionare file:line del chiamante
        stacklevel = kwargs.pop("stacklevel", 2)
        try:
            logger.debug(prefix + msg, *args, stacklevel=stacklevel, **kwargs)
        except TypeError:
            # Fallback per ambienti logging senza 'stacklevel'
            logger.debug(prefix + msg, *args, **kwargs)

    @staticmethod
    def log_info(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
        """
        Log INFO con prefisso del chiamante reale e stacklevel corretto.
        Uso: PrefixedLogger.log_info(_LOGGER, "Started %s", name)
        """
        if not logger.isEnabledFor(logging.INFO):
            return

        prefix = f"[{PrefixedLogger.caller_qualname_auto()}] "
        stacklevel = kwargs.pop("stacklevel", 2)
        try:
            logger.info(prefix + msg, *args, stacklevel=stacklevel, **kwargs)
        except TypeError:
            logger.info(prefix + msg, *args, **kwargs)

    @staticmethod
    def log_warning(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
        """
        Log WARNING con prefisso del chiamante reale e stacklevel corretto.
        Uso: PrefixedLogger.log_warning(_LOGGER, "Started %s", name)
        """
        if not logger.isEnabledFor(logging.WARNING):
            return

        prefix = f"[{PrefixedLogger.caller_qualname_auto()}] "
        stacklevel = kwargs.pop("stacklevel", 2)
        try:
            logger.warning(prefix + msg, *args, stacklevel=stacklevel, **kwargs)
        except TypeError:
            logger.warning(prefix + msg, *args, **kwargs)

    @staticmethod
    def log_error(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
        """
        Log ERROR con prefisso del chiamante reale e stacklevel corretto.
        Supporta exc_info=True per stampare lo stacktrace.
        Uso: PrefixedLogger.log_error(_LOGGER, "Boom: %s", err, exc_info=True)
        """
        if not logger.isEnabledFor(logging.ERROR):
            return

        prefix = f"[{PrefixedLogger.caller_qualname_auto()}] "
        stacklevel = kwargs.pop("stacklevel", 2)
        try:
            logger.error(prefix + msg, *args, stacklevel=stacklevel, **kwargs)
        except TypeError:
            logger.error(prefix + msg, *args, **kwargs)

    @staticmethod
    def log_exception(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
        """
        Log EXCEPTION (level ERROR) con stacktrace automatico.
        Da usare dentro un except.
        """
        if not logger.isEnabledFor(logging.ERROR):
            return

        prefix = f"[{PrefixedLogger.caller_qualname_auto()}] "
        stacklevel = kwargs.pop("stacklevel", 2)
        try:
            logger.exception(prefix + msg, *args, stacklevel=stacklevel, **kwargs)
        except TypeError:
            logger.exception(prefix + msg, *args, **kwargs)

    @staticmethod
    def exc_one_line(e: BaseException) -> str:
        """Rappresentazione in una riga di un'eccezione con file:line del punto di lancio."""
        tb = e.__traceback__
        while tb and tb.tb_next:
            tb = tb.tb_next
        if tb:
            code = tb.tb_frame.f_code
            return f"{type(e).__name__}: {e} @ {code.co_filename}:{tb.tb_lineno} in {code.co_name}"
        return f"{type(e).__name__}: {e}"

# (Opzionale) API compatibile con le vecchie funzioni:
def log_debug(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
    PrefixedLogger.log_debug(logger, msg, *args, **kwargs)

def log_info(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
    PrefixedLogger.log_info(logger, msg, *args, **kwargs)

def log_warning(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
    PrefixedLogger.log_warning(logger, msg, *args, **kwargs)

def log_error(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
    PrefixedLogger.log_error(logger, msg, *args, **kwargs)

def log_exception(logger: logging.Logger, msg: str, *args, **kwargs) -> None:
    PrefixedLogger.log_exception(logger, msg, *args, **kwargs)

def exc_one_line(e: BaseException) -> str:
    return PrefixedLogger.exc_one_line(e)
