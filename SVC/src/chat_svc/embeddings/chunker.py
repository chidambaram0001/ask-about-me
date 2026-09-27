from dataclasses import dataclass
import hashlib
import re

@dataclass
class TextChunk:
    index: int
    section: str
    content: str
    metadata: dict

class ResumeChunker:

    MAX_CHARS = 2200

    def chunk(self, text: str) -> list[TextChunk]:

        sections = self._split_sections(text)

        chunks: list[TextChunk] = []

        index = 0

        for section, content in sections:

            content = self._normalize(content)

            if not content:
                continue

            section_chunks = self._split_large_section(
                content
            )

            for chunk_content in section_chunks:

                chunks.append(
                    TextChunk(
                        index=index,
                        section=section,
                        content=chunk_content,
                        metadata={
                            "section": section,
                            "content_hash": self._hash(
                                chunk_content
                            ),
                        },
                    )
                )

                index += 1

        return chunks

    def _split_sections(
        self,
        text: str,
    ) -> list[tuple[str, str]]:

        pattern = re.compile(
            r"={5,}\n"
            r"(.*?)\n"
            r"={5,}\n",
            re.MULTILINE,
        )

        matches = list(pattern.finditer(text))

        sections = []

        for i, match in enumerate(matches):

            section_name = match.group(1).strip()

            start = match.end()

            end = (
                matches[i + 1].start()
                if i + 1 < len(matches)
                else len(text)
            )

            content = text[start:end].strip()

            sections.append(
                (
                    section_name,
                    content,
                )
            )

        return sections

    def _split_large_section(
        self,
        content: str,
    ) -> list[str]:

        if len(content) <= self.MAX_CHARS:
            return [content]

        paragraphs = content.split("\n\n")

        chunks = []
        current = ""

        for paragraph in paragraphs:

            if (
                len(current) + len(paragraph)
                <= self.MAX_CHARS
            ):
                current += (
                    "\n\n" + paragraph
                    if current
                    else paragraph
                )
            else:

                if current:
                    chunks.append(current)

                current = paragraph

        if current:
            chunks.append(current)

        return chunks

    @staticmethod
    def _normalize(text: str) -> str:

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()

    @staticmethod
    def _hash(text: str) -> str:

        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()