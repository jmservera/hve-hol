"""Language context and translations of renderer-owned interface labels."""

import html
import re
from contextlib import contextmanager
from contextvars import ContextVar
from html.parser import HTMLParser

import content


_LANGUAGE = ContextVar("language", default="en")

UI_ES = {
    "Core task": "Tarea principal",
    "Parallel task": "Tarea en paralelo",
    "Waiting-time task": "Tarea para los tiempos de espera",
    "Backup": "Reserva",
    "Exercise %s: ": "Ejercicio %s: ",
    "Exercise %s · %s": "Ejercicio %s · %s",
    "Intermission %s · %s": "Pausa %s · %s",
    "Intermission %s": "Pausa %s",
    "Backup · Exercise %s": "Reserva · Ejercicio %s",
    "%s · HVE workshop guide": "%s · Guía del taller HVE",
    "Brief": "Resumen",
    "Objective": "Objetivo",
    "Input": "Material de partida",
    "Best use": "Uso recomendado",
    "Steps": "Pasos",
    "Hand in": "Entrega",
    "Tick items as your team hands them in.": "Marca los elementos a medida que tu equipo los entregue.",
    "Entry": "Respuesta",
    "Copy as Markdown": "Copiar como Markdown",
    "Clear": "Borrar",
    "Table": "Tabla",
    "Done when": "Terminado cuando",
    "Copy": "Copiar",
    "Best for": "Ideal para",
    "Only if your team finishes early": "Solo si tu equipo termina antes",
    "Intermissions": "Pausas",
    "Intermissions and backup": "Pausas y reserva",
    "Round": "Ronda",
    "Reveal": "Ver ejemplo",
    "Write your answer in the": "Escribe tu respuesta en la",
    "answer sheet": "hoja de respuestas",
    "or on paper. Take 90 seconds; wait for the facilitator before opening the reveal.":
        "o en papel. Dedica 90 segundos; espera al facilitador antes de abrir el ejemplo.",
    "Open after answering, then score your original answer.":
        "Ábrelo después de responder y puntúa tu respuesta original.",
    "Illustrative example · fictional client and system · not a recorded run":
        "Ejemplo ilustrativo · cliente y sistema ficticios · no es una ejecución grabada",
    "Human decision:": "Decisión humana:",
    "One hand-in for Intermissions A and B": "Una entrega para las pausas A y B",
    "Template 1 · Trace from source to artefact": "Plantilla 1 · Trazabilidad de la fuente al artefacto",
    "Template 2 · Operations loop": "Plantilla 2 · Ciclo de operaciones",
    "Run it with": "Herramientas para realizarlo",
    "Rules": "Reglas",
    "(opens in a new tab)": "(se abre en una pestaña nueva)",
    "Every link from the guide in one place. Links open in a new tab.":
        "Todos los enlaces de la guía en un solo lugar. Se abren en una pestaña nueva.",
    "Accelerators": "Aceleradores",
    "Links by exercise": "Enlaces por ejercicio",
    "Templates": "Plantillas",
    "Filter links": "Filtrar enlaces",
    "Type to filter, e.g. Azure DevOps, Work IQ, squad":
        "Escribe para filtrar, por ejemplo, Azure DevOps, Work IQ, squad",
    "Resource sections": "Secciones de recursos",
    "How accelerators work": "Cómo funcionan los aceleradores",
    "Featured accelerators": "Aceleradores destacados",
    "Full catalogue": "Catálogo completo",
    "Step": "Paso",
    "Links": "Enlaces",
    "Hand-in templates": "Plantillas de entrega",
    "Skip to content": "Saltar al contenido",
    "Feedback": "Comentarios",
    "GitHub repository": "Repositorio de GitHub",
    "Quick links": "Enlaces rápidos",
    "Guide": "Guía",
    "Agenda": "Agenda",
    "Scorecard": "Evaluación",
    "Resources": "Recursos",
    "Exercise guide": "Guía de ejercicios",
    "← Guide home": "← Inicio de la guía",
    "Hand-in and toolkit": "Entrega y herramientas",
    "Tips": "Consejos",
    "On this page": "En esta página",
    "← Previous": "← Anterior",
    "← Back to": "← Volver a",
    "Guide home": "Inicio de la guía",
    "Next →": "Siguiente →",
    "Previous and next step": "Paso anterior y siguiente",
    "Breadcrumb": "Ruta de navegación",
    "Start the step-by-step guide": "Empezar la guía paso a paso",
    "Jump to an exercise": "Ir a un ejercicio",
    "Today": "Hoy",
    "This is not another presentation": "Esto no es otra presentación",
    "North-star outcome": "Resultado que nos guía",
    "How to use this guide": "Cómo utilizar esta guía",
    "Every fill-in template, by exercise.": "Todas las plantillas para completar, por ejercicio.",
    "Index": "Índice",
    "The step-by-step guide": "La guía paso a paso",
    "While agents run": "Mientras trabajan los agentes",
    "Nobody watches a progress bar. Pick up an intermission while your agents work, or see":
        "Nadie se queda mirando una barra de progreso. Realiza una pausa mientras trabajan tus agentes o consulta",
    "seven things to do while agents run": "siete cosas que hacer mientras trabajan los agentes",
    "Materials": "Materiales",
    "All links for the day are on one page, grouped by topic.":
        "Todos los enlaces del día en una página, agrupados por tema.",
    "Page not found": "Página no encontrada",
    "Page not found · HVE workshop guide": "Página no encontrada · Guía del taller HVE",
    "That page does not exist. Go back to the": "Esa página no existe. Vuelve al",
    "guide home": "inicio de la guía",
    "or the": "o a los",
    "resources": "recursos",
    "Switch to dark mode": "Cambiar al modo oscuro",
    "Switch to light mode": "Cambiar al modo claro",
}


def current_language():
    return _LANGUAGE.get()


@contextmanager
def language(value):
    if value not in ("en", "es"):
        raise ValueError("Unsupported language: %s" % value)
    token = _LANGUAGE.set(value)
    try:
        yield
    finally:
        _LANGUAGE.reset(token)


def catalog():
    if current_language() == "es":
        import content_es
        return content_es
    return content


def text(value):
    return UI_ES[value] if current_language() == "es" else value


class _InterfaceTranslator(HTMLParser):
    """Translate only interface text nodes and accessible labels, never IDs or links."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []
        self.verbatim = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("code", "pre", "script", "style"):
            self.verbatim += 1
        raw = self.get_starttag_text()
        for key, value in attrs:
            if key in ("aria-label", "placeholder", "title", "data-label-dark", "data-label-light") and value in UI_ES:
                translated = html.escape(UI_ES[value], quote=True)
                raw = re.sub(r'(\b%s=)(["\']).*?\2' % re.escape(key),
                             lambda match: '%s"%s"' % (match[1], translated), raw)
        self.parts.append(raw)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in ("code", "pre", "script", "style"):
            self.verbatim -= 1
        self.parts.append("</%s>" % tag)

    def handle_data(self, data):
        value = data.strip()
        if not self.verbatim and value in UI_ES:
            start = len(data) - len(data.lstrip())
            end = len(data.rstrip())
            data = data[:start] + html.escape(UI_ES[value], quote=False) + data[end:]
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append("&%s;" % name)

    def handle_charref(self, name):
        self.parts.append("&#%s;" % name)

    def handle_decl(self, decl):
        self.parts.append("<!%s>" % decl)

    def handle_comment(self, data):
        self.parts.append("<!--%s-->" % data)


def interface(markup):
    if current_language() == "en":
        return markup
    parser = _InterfaceTranslator()
    parser.feed(markup)
    parser.close()
    return "".join(parser.parts)
