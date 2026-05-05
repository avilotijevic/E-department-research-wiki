
# Contributing to the Wiki

This wiki is built using **Markdown files hosted on GitHub**.  
You can contribute by editing existing pages or adding new ones directly through the GitHub interface.

---

## Editing an existing page

1. Navigate to the page you want to edit in the repository.
2. Click on the file (e.g., `.md` file).
3. Click the **Edit** button (top right).
4. Make your changes using Markdown.
5. Scroll down and add a short **commit message** describing your changes.
6. Click **Commit changes**.

---

## Creating a new page

1. Navigate to the relevant folder (e.g., `methods/`, `analysis-pipelines/`).
2. Click **Add file → Create new file**.
3. Name your file using lowercase and hyphens:

`example-page.md`

4. Add content using Markdown.
5. Commit your changes.

---

## Adding the page to the sidebar

To make your page appear in the navigation menu, add the following at the top of your `.md` file: 

```yaml
title: insert-title
parent: insert-parent-folder-name
nav_order: insert-order-number
```
---

## Linking between pages

You can create links between pages using **relative paths**.

example:
[Go to EEG page]( ../parent-folder/page-that-takes-you-to-eeg . md )

---

## Adding images

### Step 1: Upload the image

1. Go to the repository on GitHub.
2. Navigate to the folder: `assets/images/`
3. Click **Add file → Upload files**.
4. Upload your image (e.g., `example.png`).
5. Commit the changes.

### Step 2: Insert the image in a page

Use the following Markdown syntax:

```md
![Description](../../assets/images/example.png)

![EEG setup](../../assets/images/eeg-setup.png)
```
