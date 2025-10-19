from graph.workflow import build_graph, StoryState

def main():
    user_input = input("Enter your story idea: ")

    graph = build_graph()
    state = StoryState(initial_prompt=user_input)

    result = graph.invoke(state)

    print("\n=== Final Story ===\n")
    print(result["story_generated"])
    print("\n=== Final Evaluation ===\n")
    print(result["evaluation"])

if __name__ == "__main__":
    main()