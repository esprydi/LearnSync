# Product Requirements Document (PRD): LearnSync – AI Study Concierge

## 1. Project Vision
To become a personal study assistant that transforms static piles of study documents (PDFs) into an active and structured learning experience using autonomous AI agent technology.

## 2. Target Users
Students or professionals who frequently face a heavy load of reading materials (long PDFs/reports) and require efficiency in understanding key concepts.

## 3. Agent Architecture (Multi-Agent System)
This application utilizes a sequential workflow where two agents work collaboratively:

### Agent 1: The Reader (Document Analysis Specialist)
*   **Responsibility:** Intake local PDF files, parse the text (especially capable of handling very long documents), and extract key entities and main bullet points.
*   **Tool:** Utilizes `FileReadTool` (as an MCP implementation) for local file access.

### Agent 2: The Tutor (Pedagogy Specialist)
*   **Responsibility:** Process the extracted data from the Reader Agent into an easy-to-understand summary and generate quiz questions for active recall.
*   **Tool:** Processes data to produce educational Markdown formatted output.

## 4. Key Features & Workflow
*   **Automated Summarization:** Converts lengthy documents into dense, concise summary points.
*   **Interactive Quiz Generation:** Creates 5 multiple-choice questions per topic to ensure comprehension (along with an answer key and explanations).
*   **Concierge Privacy:** Agents operate entirely locally, keeping your study materials strictly private.
*   **Step-by-Step Reasoning:** Displays the AI's "thinking" process in the terminal, providing transparency on how study conclusions and quizzes are generated.

## 5. Technical Implementation (For Vibe Coding)

| Component | Implementation Details |
| :--- | :--- |
| **Framework** | CrewAI (for agent orchestration) |
| **Model** | Gemini 2.5-flash (highly efficient and cost-effective for long context windows and lengthy documents) |
| **MCP Concept** | FileReadTool (for securely accessing local PDF materials) |
| **Security** | System Prompt contains instructions for safe content validation |

### Example Logic (Tutor System Prompt):
>"You are an expert academic tutor. Use the extracted results from the Reader Agent to create: (1) A summary of main concepts, (2) 5 multiple-choice quiz questions that test concept comprehension, and (3) Explanations for the answers. Ensure a supportive tone."
