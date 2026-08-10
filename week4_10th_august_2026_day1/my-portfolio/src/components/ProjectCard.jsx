function ProjectCard({ title, description, technologies, link }) {
  return (
    <article>
      <h3>{title}</h3>

      <p>{description}</p>

      <p>
        <strong>Technologies</strong>
      </p>

      <ul>
        {technologies.map((technology) => (
          <li key={technology}>{technology}</li>
        ))}
      </ul>

      <a href={link} target="_blank" rel="noreferrer">
        View Project
      </a>
    </article>
  );
}

export default ProjectCard;