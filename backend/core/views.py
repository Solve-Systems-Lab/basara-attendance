"""Views for core.

Right now there is exactly one: a health check. Everything else on the
backend backlog lives in this file too, once someone writes it.

Owner: BE track. See your track page in docs/brief.pdf.
"""

from django.http import JsonResponse


def health(request):
    """Liveness check. Day 2 checkpoint: this must return {"ok": true}.

    Deliberately dumb — it proves the process is up and the URLconf resolves,
    nothing more. On Day 5 you will be asked whether it should also check the
    database, and what status code it should return when the database is down.
    That is a real argument with two defensible sides. Have it then.
    """
    return JsonResponse({"ok": True})
