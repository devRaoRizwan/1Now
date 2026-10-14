export default function Section({ title, aside, children }) {
  return (
    <section className="section">
      <h3>
        {title}
        {aside}
      </h3>
      {children}
    </section>
  );
}
