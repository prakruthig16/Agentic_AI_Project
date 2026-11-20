
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from pydantic import ValidationError

from .models import ChatSession, ChatMessage
from .schemas import ChatRequest
from .ai_engine import generate_response


def dashboard(request):
    return render(request, "assistant/dashboard.html")


def chat_page(request):

    sessions = ChatSession.objects.order_by("-created_at")

    selected_id = request.GET.get("session")

    selected_messages = []
    selected_session_id = None

    if selected_id:
        try:
            session = ChatSession.objects.get(id=selected_id)

            selected_session_id = session.id

            selected_messages = list(
                session.messages.values("role", "content")
            )

        except ChatSession.DoesNotExist:
            pass

    return render(
        request,
        "assistant/chat.html",
        {
            "sessions": sessions,
            "selected_messages": selected_messages,
            "selected_session_id": selected_session_id,
        }
    )


@require_POST
def chat_api(request):

    try:

        data = json.loads(request.body)

        validated = ChatRequest.model_validate(data)

        question = validated.question.strip()

        if not question:
            return JsonResponse(
                {"error": "Question cannot be empty"},
                status=400
            )

        if validated.session_id:

            session = ChatSession.objects.get(
                id=validated.session_id
            )

        else:

            session = ChatSession.objects.create(
                title=question[:60]
            )

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        history = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in session.messages.all()
        ]

        history = history[:-1]

        answer = generate_response(
            question,
            history
        )

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=answer
        )

        return JsonResponse({
            "answer": answer,
            "session_id": session.id
        })

    except ValidationError as e:

        return JsonResponse(
            {"error": e.errors()},
            status=400
        )

    except ChatSession.DoesNotExist:

        return JsonResponse(
            {"error": "Conversation not found"},
            status=404
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    except Exception as e:

        return JsonResponse(
            {"error": str(e)},
            status=500
        )


def history_page(request):

    sessions = ChatSession.objects.order_by("-created_at")

    return render(
        request,
        "assistant/history.html",
        {"sessions": sessions}
    )
