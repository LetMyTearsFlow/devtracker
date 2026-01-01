import click


def note_from_external(
        initial_text: str = "",
        *,
        extension: str = ".txt",
) -> str:
    """
    open an external editor. the temp file locates in AppData/Local/Temp
    - initial_text: prefilled content
    - extension: extension
    - require_non_empty: requires non-empty content
    """
    while True:
        edited = click.edit(
            text=initial_text,
            extension=extension,
        )
        # edited: str | None
        # None represent no input
        if edited is None:
            return initial_text

        lines = edited.split("\n")
        result = "\n".join([line for line in lines if not line.startswith("#")])

        return result
