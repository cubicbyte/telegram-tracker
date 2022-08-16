import prompts from 'prompts'

export default function prompt(question: prompts.PromptObject): () => Promise<string> {
    return async function() {
        const result = await prompts(question, {
            onCancel() {
                process.exit(0)
            }
        })
        
        return result[question.name as keyof prompts.Answers<string>]
    }
}
