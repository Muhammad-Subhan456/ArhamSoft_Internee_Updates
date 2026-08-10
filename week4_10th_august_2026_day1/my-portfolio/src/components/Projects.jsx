import ProjectCard from "./ProjectCard";

function Projects() {
  return (
    <section id="projects" aria-labelledby="projects-heading">
      <h2 id="projects-heading">Projects</h2>

      <div className="projects-grid">
        

        <ProjectCard
          title="Microservices Ticketing App"
          description="A microservices-based ticketing platform with event-driven communication and containerized deployment."
          technologies={[
            "Node.js",
            "TypeScript",
            "Docker",
            "Kubernetes",
            "NATS",
          ]}
          link="https://github.com/Muhammad-Subhan456/Microservices_Ticketing_App"
        />

        <ProjectCard
          title="Business Analyzer Agent"
          description="An AI-powered multi-agent system for automated business analysis and research."
          technologies={[
            "Python",
            "CrewAI",
            "LLMs",
            "Streamlit",
          ]}
          link="https://github.com/Muhammad-Subhan456/Business_Analyzer_Agent"
        />
        <ProjectCard
          title="Notes API"
          description="A RESTful Notes API with authentication, authorization, PostgreSQL, and Docker."
          technologies={[
            "FastAPI",
            "PostgreSQL",
            "SQLAlchemy",
            "Docker",
          ]}
          link="https://github.com/Muhammad-Subhan456/ArhamSoft_Internee_Updates/tree/main/week3_4th_august_2026_Thursday"
        />
      </div>
    </section>
  );
}

export default Projects;