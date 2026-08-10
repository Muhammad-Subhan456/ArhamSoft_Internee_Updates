# Personal Portfolio — React + Vite

A modern, responsive personal portfolio website built with **React** and **Vite**.  
The project was developed as part of the React learning and practical kata exercises, focusing on componentization, props, semantic HTML, accessibility, forms, and responsive CSS.

## 🌐 Live Demo

**Deployed Application:**  
https://portfolio-sepia-two-ca7eld96sd.vercel.app/

---

## 📌 About the Project

This portfolio presents my profile, skills, projects, and contact information through a clean and responsive interface.

The project demonstrates how a frontend application can be structured using reusable React components instead of building the entire page as one component.

---

## ✨ Features

- Responsive modern portfolio design
- Hero section with professional profile image
- About Me section
- Skills section
- Projects section with reusable project cards
- Contact form
- Native HTML form validation
- Accessible form labels
- Radio button group using `<fieldset>` and `<legend>`
- Keyboard-friendly navigation
- Semantic HTML structure
- Responsive layout for desktop, tablet, and mobile
- Smooth scrolling
- Hover and focus states
- Reusable React components

---

## 🛠️ Technologies Used

- React
- Vite
- JavaScript
- HTML5
- CSS3
- ESLint

---

## 📂 Project Structure

```text
project-root/
│
├── public/
│   └── profile.jpg
│
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Home.jsx
│   │   ├── Projects.jsx
│   │   ├── ProjectCard.jsx
│   │   ├── Contact.jsx
│   │   └── Footer.jsx
│   │
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── .gitignore
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
└── README.md