# Data rules

## Overview

This document serves as a living document around standards TinyDevCRM should
respect in its data model, with respect to database, backend, and frontend
representation where possible.

## Rules

-   **All timestamps should be stored as
    [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601), normalized to
    UTC+00:00.** Timezones should be stored separately, and merged with other
    data (e.g. user preferences) to generate a specific view.

-   **Module docstrings should follow the [reStructured
    Text](https://en.wikipedia.org/wiki/ReStructuredText) specification, as per
    [PEP-287](https://www.python.org/dev/peps/pep-0287/).**

-   **Floating point values should be stored as
    [IEEE-754](https://en.wikipedia.org/wiki/IEEE_754).** Ideally, values should
    not be represented as floating point except in final views, due to the
    inaccuracy of floating point hardware resulting in value drift based on
    calculation pipeline length (e.g. billing pipelines should use integers in
    the finest granularity of the applicable currency), and performance penalties
    of floating point calculations.

-   **Strings should be encoded in
    [Unicode](https://en.wikipedia.org/wiki/Unicode), and as
    [UTF-8](https://en.wikipedia.org/wiki/UTF-8) where possible.**
