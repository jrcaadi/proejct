import openai

openai.api_key = '..'

def get_input(prompt_text, valid_options=None, validation_func=None):
    while True:
        user_input = input(prompt_text)
        if valid_options and user_input not in valid_options:
            print(f"Invalid input. Please choose from {valid_options}.")
        elif validation_func and not validation_func(user_input):
            print("Invalid input. Please try again.")
        else:
            return user_input

def generate_project_ideas():
    field = get_input("Which field (closest SDG) that links to it if applicable? ")
    budget = get_input("Budget? ")
    group_size = get_input("Group size? ", validation_func=lambda x: x.isdigit() and int(x) > 0)
    planned_scale = get_input("Planned scale to reach? ")
    project_description = get_input("Project description/specifications/requirements? ")
    purpose = get_input("Purpose? ")
    audience = get_input("Audience? ")

    answers = f"Field: {field}\nBudget: {budget}\nGroup size: {group_size}\nPlanned scale: {planned_scale}\nProject description: {project_description}\nPurpose: {purpose}\nAudience: {audience}"
    prompt = f"""
    Student answers:
    {answers}

    Generate 10 specific and detailed project ideas based on these answers. For each project, include:

    1. Brief description: Define goals and core concept.
    2. Expected impact: Short-term and long-term benefits.
    3. Necessary resources: Materials, human resources, and technology.
    4. Execution plan: Key steps and timeline.
    5. Challenges: Potential risks and mitigation strategies.
    6. Budget: Cost estimates and funding sources.
    7. Success metrics: Criteria and measurement methods.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing detailed and specific project ideas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        ideas = response['choices'][0]['message']['content'].strip()
        return ideas
    except Exception as e:
        print(f"An error occurred while generating project ideas: {e}")
        return None

def get_in_depth_knowledge(chosen_project):
    prompt = f"""
    Provide an in-depth, step-by-step guide for executing the project: {chosen_project}. The guide should include the following comprehensive details:

    1. Planning Phase:
       a. Define the project scope and specific objectives in detail.
       b. Identify and describe key stakeholders and their roles and responsibilities.
       c. Develop a detailed project plan, including a Gantt chart or similar timeline.
       d. Create a comprehensive risk management plan, including risk identification, assessment, and mitigation strategies.

    2. Resource Allocation:
       a. List all necessary resources in detail, including materials, human resources, technology, and facilities.
       b. Develop a detailed budget plan, itemizing all costs and funding sources.
       c. Assign tasks and responsibilities to team members, detailing their roles and expectations.

    3. Execution Phase:
       a. Provide a step-by-step breakdown of tasks and activities required to execute the project.
       b. Identify key milestones and deliverables, specifying their importance and deadlines.
       c. Detail monitoring and reporting mechanisms to track progress and ensure accountability.
       d. Develop a communication plan to keep stakeholders informed and engaged throughout the project.

    4. Potential Obstacles:
       a. Identify potential risks and challenges in detail, including their likelihood and impact.
       b. Develop comprehensive contingency plans for each identified risk.
       c. Propose strategies and solutions for overcoming common obstacles, drawing on best practices and case studies.

    5. Evaluation and Improvement:
       a. Define clear success metrics and explain how to measure them effectively.
       b. Conduct a post-project evaluation, including collecting feedback from stakeholders and team members.
       c. Document lessons learned and best practices to inform future projects, providing detailed examples and recommendations.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing detailed and specific project execution steps."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        in_depth_knowledge = response['choices'][0]['message']['content'].strip()
        return in_depth_knowledge
    except Exception as e:
        print(f"An error occurred while retrieving in-depth knowledge: {e}")
        return None

def chat():
    print("Great! Now you can ask any questions")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Thank you for chatting!")
            break
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an experienced counselor who gives very detailed and informative advice to the users. You have the knowledge and scale the projects on local, national, and international levels and cater completely to the needs of the user. When you are giving your advice, always remember that he is a student who wants to develop a project and is coming to you to create a plan of action for the future. When you are giving advice, also remember that you have a community called Projectify. Find the best time to pitch them to this community but do it only once in one conversation."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            print("Chatbot:", response['choices'][0]['message']['content'])
        except Exception as e:
            print(f"An error occurred during the chat: {e}")

project_ideas = generate_project_ideas()
if project_ideas:
    print("Generated Project Ideas:\n", project_ideas)
    chosen_project = get_input("Choose a project idea (copy and paste the title): ")
    in_depth_knowledge = get_in_depth_knowledge(chosen_project)
    if in_depth_knowledge:
        print("\nIn-depth Knowledge:\n", in_depth_knowledge)
        chat()
else:
    print("Failed to generate project ideas.")
