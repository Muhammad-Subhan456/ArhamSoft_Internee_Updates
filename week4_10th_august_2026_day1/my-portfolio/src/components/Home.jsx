function Home() {
  return (
    <main id="home">
      <section className="hero" aria-labelledby="hero-heading">
        <div className="hero-content">
          <p className="hero-eyebrow">Software Engineer · AI/ML</p>

          <h2 id="hero-heading">Hi, I'm Subhan.</h2>

          <p className="hero-summary">
            I build scalable software, AI-powered applications, and
            well-structured systems that solve real-world problems.
          </p>

          <a className="hero-button" href="#projects">
            View My Projects
          </a>
        </div>

        <div className="hero-image">
          <img
            src="/Me.png"
            alt="Professional portrait of Subhan"
          />
        </div>
      </section>

      <section
        className="about-section"
        aria-labelledby="about-heading"
      >
        <h2 id="about-heading">About Me</h2>

        <p>
        I am a Software Engineer who enjoys building scalable, well-structured systems that solve real-world problems.
My work spans backend and full-stack development, with a focus on microservices, system design, and
performance optimization. I have solved 800+ problems on LeetCode and Codeforces and earned a Silver Medal
in ICPC Asia West Topi Region’26, reflecting strong problem-solving skills. I take pride in turning
complex challenges into clean, maintainable solutions that improve reliability and efficiency.
        </p>
      </section>

      <section
        className="skills-section"
        aria-labelledby="skills-heading"
      >
        <h2 id="skills-heading">Skills</h2>

        <ul>
          <li>Python</li>
          <li>JavaScript</li>
          <li>React</li>
          <li>FastAPI</li>
          <li>Node.js</li>
          <li>PostgreSQL</li>
          <li>Docker</li>
          <li>Kubernetes</li>
          <li>AI/ML</li>
          <li>LLMs</li>
        </ul>
      </section>
    </main>
  );
}

export default Home;