def retrieve_relevant_characters(chapter_goal, characters_text):
    relevant = []
    for block in characters_text.split("# 角色卡"):
        if any(name in chapter_goal for name in ["沈砚", "阿禾", "赵烬"]):
            relevant.append(block)
    return "\n".join(relevant)

