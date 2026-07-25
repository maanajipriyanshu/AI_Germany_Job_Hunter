from providers.gemini_provider import GeminiProvider


class CoverLetter:

    provider = GeminiProvider()

    @staticmethod
    def humanize(
        cover_letter,
        style="German Corporate"
    ):

        return CoverLetter.provider.rewrite_cover_letter(
            cover_letter,
            style
        )