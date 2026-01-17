#
from __future__ import annotations

from typing import TypeVar, Type, Any, Literal, Callable
from dataclasses import is_dataclass, fields as dc_fields, MISSING
from inspect import Parameter, signature
import math
import re
from decimal import Decimal

from homeassistant.core import State as HAState
from homeassistant.const import STATE_UNKNOWN, STATE_UNAVAILABLE

TRUE_STRINGS: set[str] = {"1", "true", "t", "yes", "y", "on"}
FALSE_STRINGS: set[str] = {"0", "false", "f", "no", "n", "off", ""}

_NUM_RE = re.compile(r"[-+]?\d+(?:[.,]\d+)?")

def _first_number_token(text: str) -> str | None:
    """
    Estrae il primo token numerico da una stringa (supporta '.' o ',' come separatore decimale).
    Esempi: "23.5°C" -> "23.5", "umidità 45,2 %" -> "45,2"
    """
    m = _NUM_RE.search(text)
    return m.group(0) if m else None

def _clamp[T: (int|float)](value: T, min_value: T | None, max_value: T | None) -> T:
    if min_value is not None and value < min_value:
        value = min_value
    if max_value is not None and value > max_value:
        value = max_value
    return value

def as_bool(
    v: Any,
    default: bool | None = None,
    *,
    strict: bool = False,
) -> bool | None:
    """
    Converte input in bool.
    - bool: restituito com'è
    - int/float/Decimal: 0 => False, !=0 => True
    - str: case-insensitive, supporta {1,true,t,yes,y,on} / {0,false,f,no,n,off,""}
    - None: restituisce 'default' (o ValueError se strict)
    """
    if v is None:
        if strict:
            raise ValueError("Cannot coerce None to bool")
        return default

    if isinstance(v, bool):
        return v

    if isinstance(v, (int, float, Decimal)):
        return (float(v) != 0.0)

    if isinstance(v, str):
        s = v.strip().lower()
        if s in TRUE_STRINGS:
            return True
        if s in FALSE_STRINGS:
            return False

    if strict:
        raise ValueError(f"Cannot coerce {v!r} to bool")
    return default

def ratio_or_percent_to_int(v: float | None) -> int | None:
    """
    Converte un valore percentuale espresso come frazione in [0..1]
    *oppure* già in percento [0..100] in un intero compreso tra 0 e 100.

    Regole:
    - `None` → `None`
    - `NaN`/±`inf` → `None`
    - Valori in [0..1] (con piccola tolleranza) sono interpretati come frazione e moltiplicati ×100.
    - Altri valori sono interpretati come percento già espresso.
    - Clamping finale a [0, 100] e arrotondamento al più vicino intero.

    Esempi:
    >>> _pct01_to_pct100_int(None) is None
    True
    >>> _pct01_to_pct100_int(0.456)
    46
    >>> _pct01_to_pct100_int(1.0)
    100
    >>> _pct01_to_pct100_int(72.3)
    72
    >>> _pct01_to_pct100_int(-0.1)   # clamp a 0
    0
    >>> _pct01_to_pct100_int(123.4)  # clamp a 100
    100
    >>> _pct01_to_pct100_int(float("nan")) is None
    True
    """
    if v is None or not math.isfinite(v):
        return None

    # Tolleranza per errori floating (es. 1.0000000002)
    _EPS = 1e-9
    if -_EPS <= v <= 1.0 + _EPS:
        v *= 100.0

    # Clamp e arrotondamento
    v = max(0.0, min(100.0, v))
    return int(round(v))

def as_float(
    v: Any,
    default: float | None = None,
    *,
    min_value: float | None = None,
    max_value: float | None = None,
    strict: bool = False,
) -> float | None:
    """
    Converte input in float.

    Supporta:
      - float/int/Decimal → cast diretto
      - bool → 1.0/0.0
      - str → estrae il primo numero (accetta '.' o ','); ignora unità attigue
      - homeassistant.core.State → usa `state.state` (salta 'unknown'/'unavailable')
      - None → `default` (o eccezione se `strict=True`)

    Applica clamp opzionale con min/max.
    Rifiuta NaN/Inf (ritorna default o alza in strict).
    """
    if v is None:
        if strict:
            raise ValueError("Cannot coerce None to float")
        return default

    try:
        # Caso: Home Assistant State
        if isinstance(v, HAState):
            s = v.state
            if s in (STATE_UNKNOWN, STATE_UNAVAILABLE, None, ""):
                if strict:
                    raise ValueError(f"Cannot coerce HA State '{s}' to float")
                return default
            v = s  # prosegui come per stringa

        # Primitive e numerici
        if isinstance(v, bool):
            x = 1.0 if v else 0.0
        elif isinstance(v, float):
            x = v
        elif isinstance(v, int):
            x = float(v)
        elif isinstance(v, Decimal):
            x = float(v)
        elif isinstance(v, str):
            token = _first_number_token(v.strip())
            if token is None:
                raise ValueError("no numeric token")
            token = token.replace(",", ".")  # normalizza separatore decimale
            x = float(token)
        else:
            raise TypeError(f"unsupported type: {type(v).__name__}")

        # Scarta NaN/Inf
        if not math.isfinite(x):
            raise ValueError("non-finite float")

    except Exception:
        if strict:
            raise
        return default

    return _clamp(x, min_value, max_value)

def as_int(
    v: Any,
    default: int | None = None,
    *,
    min_value: int | None = None,
    max_value: int | None = None,
    strict: bool = False,
    rounding: str = "nearest",  # "nearest" | "floor" | "ceil" | "truncate"
) -> int | None:
    """
    Converte input in int.
    - int: restituito com'è
    - float/Decimal/str numerica: convertiti secondo 'rounding'
      • nearest  -> round(x)
      • floor    -> math.floor(x)
      • ceil     -> math.ceil(x)
      • truncate -> int(x) (taglia verso zero)
    - str con unità: estrae primo numero come _as_float
    - None: -> default (o ValueError se strict)
    Applica clamp opzionale con min/max.
    """
    if v is None:
        if strict:
            raise ValueError("Cannot coerce None to int")
        return default

    import math

    # percorso veloce
    if isinstance(v, int):
        x = v
    else:
        xf = as_float(v, None, strict=strict)
        if xf is None:
            return default
        if rounding == "nearest":
            x = int(round(xf))
        elif rounding == "floor":
            x = math.floor(xf)
        elif rounding == "ceil":
            x = math.ceil(xf)
        elif rounding == "truncate":
            x = int(xf)
        else:
            if strict:
                raise ValueError(f"Unknown rounding mode: {rounding}")
            x = int(round(xf))

    x = _clamp(x, min_value, max_value)
    return x

def slugify(text: str) -> str:
    """
    Converte una stringa in uno *slug* semplice e sicuro per identificatori/URL.

    Regole:
    - Converte tutto in minuscolo.
    - Mantiene solo caratteri alfanumerici (Unicode) tramite `str.isalnum()`.
      (Esempio: lettere accentate come "à" vengono mantenute.)
    - Sostituisce spazio, trattino `-` e underscore `_` con un underscore `_`.
    - Rimuove eventuali underscore iniziali/finali.

    Nota: non effettua normalizzazione ASCII né il collasso di underscore consecutivi.

    Args:
        text: La stringa di input.

    Returns:
        Uno slug derivato da `text`.

    Esempi:
        >>> slugify("Hello, World!")
        'hello_world'
        >>> slugify("  già-pronto  ")
        'già_pronto'
        >>> slugify("A__B  C-D")
        'a__b__c_d'
        >>> slugify("__titolo__")
        'titolo'
    """
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "-", "_"):
            out.append("_")
    slug = "".join(out).strip("_")
    return slug

def computed_float_or_none(
    value_or_fn: Any | Callable[[], Any],
    *,
    precision: int | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
    strict: bool = False,
) -> float | None:
    """
    Prova a calcolare/coercizzare un valore numerico in float.

    - Se `value_or_fn` è callable -> lo esegue e usa il risultato.
    - Altrimenti usa direttamente `value_or_fn`.
    - Converte con `as_float(...)` (gestisce anche Home Assistant State).
    - Applica clamp (min/max) e rounding opzionale.
    - In caso di errori o valore non numerico -> None (o eccezione se strict=True).

    Args:
        value_or_fn: valore o funzione che ritorna un valore.
        precision: cifre decimali per round (None = nessun round).
        min_value, max_value: clamp opzionale.
        strict: se True, propaga eccezioni di parsing.

    Returns:
        float | None
    """
    try:
        raw = value_or_fn() if callable(value_or_fn) else value_or_fn
    except Exception:
        if strict:
            raise
        return None

    x = as_float(
        raw,
        default=None,
        min_value=min_value,
        max_value=max_value,
        strict=strict,
    )
    if x is None:
        return None

    if precision is not None:
        try:
            x = round(float(x), precision)
        except Exception:
            x = float(x)
    return x


T = TypeVar("T")
def make_class(cls: Type[T], /, *, drop_none: bool = True, strict: bool = True, **values: Any) -> T:
    """
    Crea un'istanza della classe ``cls`` usando solo i kwargs compatibili, con
    possibilità di **filtrare i valori None** e **validare** campi/argomenti richiesti.

    La funzione supporta sia:
      - **dataclass**: determinazione dei campi ammessi e di quelli obbligatori
        tramite introspezione dei metadati (``dataclasses.fields``).
      - **classi normali**: ispezione della ``__init__`` signature per validare
        argomenti richiesti e individuare eventuali extra non previsti.

    Parametri
    ----------
    cls : Type[T]
        La classe da istanziare (dataclass o classe “normale”).
    drop_none : bool, default ``True``
        Se ``True``, rimuove dai kwargs le coppie con valore ``None`` prima della validazione.
        Utile quando certi campi sono opzionali e hanno default nella classe.
    strict : bool, default ``True``
        Se ``True``, segnala come errore eventuali kwargs **non previsti** dalla classe.
        - Per **dataclass**, gli extra non compaiono tra i ``fields``.
        - Per **classi normali**, gli extra sono consentiti solo se la signature di
          ``__init__`` accetta ``**kwargs``; altrimenti viene sollevato ``TypeError``.
    **values : Any
        I kwargs da passare al costruttore di ``cls``. Possono includere campi opzionali
        con ``None`` (che verranno rimossi se ``drop_none=True``).

    Ritorna
    -------
    T
        L'istanza creata di tipo ``cls``.

    Solleva
    -------
    TypeError
        - Se **mancano** campi/argomenti **obbligatori** (dataclass: campi senza default;
          classi normali: parametri senza default nella signature).
        - Se sono presenti kwargs **non previsti** e ``strict=True`` (salvo che la
          signature consenta ``**kwargs`` per classi normali).

    Note
    ----
    - La funzione passa **solo argomenti per parola chiave** al costruttore.
      Parametri posizionali (``*args``) non sono composti da questa utility.
    - Il filtro su ``None`` usa ``is not None``: valori falsy come ``0``, ``0.0`` e
      ``False`` **non** vengono rimossi.
    - Per dataclass, un campo è considerato obbligatorio se il suo ``default`` è
      ``MISSING`` **e** il suo ``default_factory`` è ``MISSING``.

    Esempi
    -------
    Dataclass:
    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Snap:
    ...     ts: int
    ...     t: float | None = None
    ...     active: bool = False
    ...
    >>> make_class(Snap, ts=123, t=None, active=True)
    Snap(ts=123, t=None, active=True)

    Classe normale:
    >>> class C:
    ...     def __init__(self, x, y=0, *, z):
    ...         self.x, self.y, self.z = x, y, z
    ...
    >>> make_class(C, x=1, z=3, y=None)   # y=None viene rimosso se drop_none=True
    <__main__.C object at ...>
    """
    if drop_none:
        values = {k: v for k, v in values.items() if v is not None}

    if is_dataclass(cls):
        # --- dataclass: conosciamo i campi e quelli obbligatori
        allowed = {f.name for f in dc_fields(cls)}
        cleaned = {k: v for k, v in values.items() if k in allowed}

        required = {
            f.name for f in dc_fields(cls)
            if f.default is MISSING and f.default_factory is MISSING
        }
        missing = required - cleaned.keys()
        if missing:
            raise TypeError(f"{cls.__name__}: missing required fields {sorted(missing)}")

        if strict and (extra := set(values) - allowed):
            raise TypeError(f"{cls.__name__}: unexpected fields {sorted(extra)}")

        return cls(**cleaned)  # type: ignore[arg-type]

    # --- classe "normale": ispeziona la signature di __init__
    sig = signature(cls)
    params = {n: p for n, p in sig.parameters.items() if n != "self"}
    accepts_kwargs = any(p.kind == Parameter.VAR_KEYWORD for p in params.values())

    if strict and not accepts_kwargs:
        extra = set(values) - set(params)
        if extra:
            raise TypeError(f"{cls.__name__}: unexpected args {sorted(extra)}")

    required = {
        n for n, p in params.items()
        if p.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
        and p.default is Parameter.empty
    }
    missing = required - set(values)
    if missing:
        raise TypeError(f"{cls.__name__}: missing required args {sorted(missing)}")

    if not accepts_kwargs:
        values = {k: v for k, v in values.items() if k in params}

    return cls(**values)

def pad(
    s: str,
    width: int,
    *,
    align: Literal["left", "right", "center"] = "left",
    fill: str = " ",
    truncate: bool = False,
    ellipsis: str = "…",
) -> str:
    """
    Restituisce `s` portata a lunghezza `width` con padding e allineamento scelti.

    Parametri
    ---------
    s : str
        Testo sorgente.
    width : int
        Larghezza desiderata (numero di caratteri). Se <= 0, ritorna stringa vuota.
    align : {"left","right","center"}, default "left"
        Allineamento del testo dentro il campo.
    fill : str, default " "
        Pattern di riempimento (può avere lunghezza > 1; verrà ripetuto e tagliato).
    truncate : bool, default False
        Se True e `len(s) > width`, tronca `s` per farla rientrare.
    ellipsis : str, default "…"
        Ellissi da usare in troncamento (se `truncate=True`).

    Ritorna
    -------
    str
        Stringa paddata (o troncata).

    Note
    ----
    - Se `truncate=False` e `len(s) > width`, la stringa originale è restituita (non troncata).
    - Per monospace/log è spesso comodo `fill=" "` o `fill="·"`.
    """
    if width <= 0:
        return ""

    n = len(s)
    if n == width:
        return s

    if n > width:
        if not truncate:
            return s
        # Troncamento con ellissi
        if width <= len(ellipsis):
            return ellipsis[:width]
        keep = width - len(ellipsis)
        if align == "left":
            return s[:keep] + ellipsis
        elif align == "right":
            return ellipsis + s[-keep:]
        else:  # center: conserva testa e coda
            left_keep = keep // 2
            right_keep = keep - left_keep
            return s[:left_keep] + ellipsis + s[-right_keep:]

    # Qui n < width: serve padding
    missing = width - n
    if not fill:
        fill = " "  # fallback

    def make_pad(k: int) -> str:
        # ripeti il pattern e taglia alla lunghezza richiesta
        times = (k + len(fill) - 1) // len(fill)
        return (fill * times)[:k]

    if align == "left":
        return s + make_pad(missing)
    elif align == "right":
        return make_pad(missing) + s
    else:  # center
        left = missing // 2
        right = missing - left
        return make_pad(left) + s + make_pad(right)


