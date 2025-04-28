// This module provides a function to render markdown as HTML using the marked.js library.
// Include the marked.js library by downloading it from https://cdnjs.com/libraries/marked

function renderMarkdownToHTML(markdown) {
    // Use the marked library from the global window object to convert markdown to HTML
    return window.marked.marked(markdown);
}

export { renderMarkdownToHTML };