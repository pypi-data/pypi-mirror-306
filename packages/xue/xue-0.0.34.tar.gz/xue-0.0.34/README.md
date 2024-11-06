# Xue

[English](README.md) | [Chinese](README_CN.md)

Xue (show, [ˈʃəʊ]) is a minimalist front-end web framework for quickly building simple web applications. This project is inspired by [FastHTML](https://github.com/AnswerDotAI/fasthtml). FastHTML is very useful, but when I was building my blog application, I found that I couldn't solve some bugs related to markdown rendering. Therefore, I decided to write a minimalist web framework myself. I don't like using other people's frameworks because if I encounter problems, I won't know how to solve them. If you, like me, use Python as your development language, I think Xue is suitable for you to quickly develop web applications.

## Install

```bash
pip install xue
```

## Use

You can use xue to build a simple todo list web application with only 50 lines of code, as follows:

```python
import uuid
from xue import *
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Form as fastapiForm, HTTPException

app = FastAPI()

# Simulated database
todos = []

class Todo(BaseModel):
    id: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    result = HTML(
        Head(
            Title("HTMX Todo App"),
        ),
        Body(
            H1("HTMX Todo App"),
            Form(
                Input(type="text", name="content", placeholder="Enter a new todo", required="required"),
                Button("Add Todo", type="submit"),
                hx_post="/todos",
                hx_target="#todo-list",
                hx_swap="beforeend"
            ),
            Ul(id="todo-list")
        )
    ).render()

    return result

@app.post("/todos", response_class=HTMLResponse)
async def create_todo(content: str = fastapiForm(...)):
    todo = Todo(id=str(uuid.uuid4()), content=content)
    todos.append(todo)
    return Li(
        todo.content,
        Button("Delete", hx_delete=f"/todos/{todo.id}", hx_target=f"#todo-{todo.id}", hx_swap="outerHTML"),
        id=f"todo-{todo.id}"
    ).render()

@app.delete("/todos/{todo_id}", response_class=HTMLResponse)
async def delete_todo(todo_id: str):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return ""
    raise HTTPException(status_code=404, detail="Todo not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Component

Xue provides some simple components that you can use to build your web applications.

The components currently written are: button, checkbox, dropdown, form, input, select. Styling is done using tailwindcss. It mimics the shadcn/ui component library, including smooth dynamic effects, elegant, simple, and aesthetically pleasing interfaces, smooth animations, and responsive interactions.

## LLM friendly

Since this is a new framework, if asked, the current LLM will not provide effective suggestions, so I have written a script to automatically generate LLM-friendly documentation. You can use the following command to generate LLM-friendly documentation:

```bash
python llm_context.py
```

The script will automatically save the document in the `llm_context.txt` file. You can directly copy it to LLM for effective advice.

## Tailwind CSS

The JIT (Just-In-Time) mode of Tailwind CSS, here are the implementation steps:

1. Install necessary dependencies:

```bash
npm init -y
npm install tailwindcss@latest postcss@latest autoprefixer@latest
```

2. Create Tailwind CSS configuration file:

```bash
npx tailwindcss init -p
```

This will create the `tailwind.config.js` and `postcss.config.js` files.

3. Modify `tailwind.config.js`:

```javascript
module.exports = {
  mode: 'jit',
  purge: [
    './templates/**/*.html',
    './static/**/*.js',
    './your_python_file.py',  // File containing your Python code
  ],
  darkMode: false,
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
```

4. Create an `input.css` file:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

5. Add an npm script to `package.json`:

```json
"scripts": {
  "build-css": "tailwindcss -i ./input.css -o ./static/styles.css --watch"
}
```

6. Run build script:

```bash
npm run build-css
```

This will start a monitoring process that regenerates the CSS whenever your Python file changes.