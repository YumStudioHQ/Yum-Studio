# YumStudio

**YumStudio** is a *meta-game engine* built on top of [Godot](https://godotengine.org/), with the goal of extending its core to support multiple languages and deeper control over engine behavior.

It is not just a framework — it’s an experimental layer over Godot designed to push its boundaries and introduce new levels of flexibility, modularity, and interoperability.

---

## Vision

YumStudio aims to:

* Provide full **C**, **C++**, **Lua**, and **C#** integration directly inside Godot.
* Allow developers to create **custom Godot Node types** using a safer, layered API.
* Offer an engine that is **meta** — capable of reconfiguring and rebuilding itself through its own development tools.
* Simplify **engine customization**, **plugin development**, and **native integration** without depending heavily on C#.

This project is a personal long-term effort to build a system where creators have complete control over both gameplay logic and the underlying engine.

---

## Developer Tools

### YumStudio-Developers (CLI)

YumStudio includes a developer command-line tool:
[`ysdev.py`](./ysdev.py)

It handles installation, updates, builds, and validation tasks for the engine.

For detailed usage, see [ysdev-doc.md](./doc/ysdev-doc.md).

---

## Author’s Note

> *“Coding a meta-game engine is hard — and often exhausting.
> I’ve been doing it mostly alone: tests, documentation, APIs, UI design…
> It’s long and sometimes frustrating, but it’s also deeply meaningful.
> My dream is to make Godot truly embrace the C and C++ languages —
> not just as add-ons, but as first-class citizens.”*
>
> — **モノエ / MONOE**, creator of YumStudio

---

## Other

* [License](./LICENSE)
* [Authors](./AUTHORS.md)
* [Credits](./CREDITS.md)

---

## Project Status

This project is under **active development** and still in an experimental phase.
Expect major changes as the architecture evolves to support more languages and tighter Godot integration.
