class FeedbackSystem:
    def __init__(self, correct_answer, hints=None, explanations=None):
        self.correct_answer = correct_answer
        self.hints = hints if hints else []
        self.explanations = explanations if explanations else {}

    def check_answer(self, user_answer):
        """Compara la respuesta del usuario con la correcta y devuelve feedback."""
        is_correct = user_answer.strip().lower() == self.correct_answer.strip().lower()
        feedback = {
            "correct": is_correct,
            "hint": self._get_hint(is_correct),
            "explanation": self._get_explanation(is_correct)
        }
        return feedback

    def _get_hint(self, is_correct):
        """Devuelve una sugerencia si la respuesta es incorrecta."""
        if not is_correct and self.hints:
            return self.hints[0]  # Puedes mejorar esto para rotar sugerencias
        return "¡Bien hecho! Continúa así."

    def _get_explanation(self, is_correct):
        """Devuelve una explicación si la respuesta es incorrecta."""
        if not is_correct and self.explanations:
            error_type = "general"  # Puedes personalizar según el tipo de error
            return self.explanations.get(error_type, "Revisa tu consulta SQL.")
        return "Respuesta correcta."