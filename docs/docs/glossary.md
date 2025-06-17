# Glossary

- **Ingestion** – the process of reading a new item from the stream and deciding whether or not to store it.
- **Lookup** – recovering the original stream index at which a stored item arrived.
- **S** – shorthand for surface size, i.e. the number of storage sites available.
- **Site** – a location in memory where one item may be stored.
- **Steady** – downsample distribution maintaining uniform spacing between retained items.
- **Stretched** – distribution that thins proportionally to depth in the stream, emphasizing older data.
- **T** – count of elapsed items in the stream.
- **Tilted** – distribution that thins proportionally to age, emphasizing recent data.
- **Surface** – collection of all sites comprising the fixed-capacity buffer.
- **Hybrid algorithm** – algorithm combining multiple distributions by partitioning the surface among them.
- **dstream_version** – metadata identifier stored alongside serialized data for compatibility checks.
