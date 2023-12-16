from django.shortcuts import render
import openai

def query(request):
    if request.method == 'POST':
        api_key = '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'
        prompt = request.POST.get('prompt', '')

        # Initialize OpenAI's GPT-3 client
        openai.api_key = api_key

        # Your GPT-3 query
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )

        context = {
            'response': response.choices[0].text.strip(),
            'prompt': prompt
        }
        return render(request, 'query.html', context)
    else:
        return render(request, 'query.html')
