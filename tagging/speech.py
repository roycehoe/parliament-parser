def get_speech_tagged_handsard(handsard_lines_data: list[dict]):
    result: list[dict] = []

    for line_data in handsard_lines_data:
        if line_data["speaker"] is None:
            result.append({**line_data, "speech": None})
            continue
        result.append(
            {
                **line_data,
                "speech": line_data["raw_text"].replace(line_data["speaker"], ""),
            }
        )

    return result
