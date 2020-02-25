# Flight rules

## What are flight rules?

A guide for core developers and core maintainers of `tinydevcrm-dashboard` about
what to do when things go wrong.

>   *Flight rules* are the hard-earned body of knowledge recorded in manuals
>   that list, step-by-step, what to do if X occurs, and why. Essentially, they
>   are extremely detailed, scenario-specific standard operating procedures.
>
>   NASA has been capturing our missteps, disasters, and solutions since the
>   early 1960s, when Mercury-era ground teams first started gathering "lessons
>   learned" into a compendium that now lists thousands of problematic
>   situations, from engine failure to busted hatch handles to computer
>   glitches, and their solutions.

-- Chris Hadfield, *An Astronaut's Guide to Life*.

## 1. `psql` connections to AWS RDS instances time out

### Problem

I deployed a PostgreSQL instance on Amazon Web Services (AWS) Relational
Database Service (RDS) with the intention to test whether extension `pg_cron`
could be created, and whether it was indeed supported by AWS, as per [this blog
post](https://www.alibabacloud.com/help/doc-detail/150355.htm) by Alibaba Cloud
discussing `pg_cron` configuration on AWS RDS last updated on February 24th of
this year (2020). Using `pg_cron` is imperative to TinyDevCRM as it enables
automated event generation, and precludes a need to consider a hybrid cloud
approach (Citus Cloud supports `pg_cron`, but since Citus Data was acquired by
Microsoft, it is only available via Azure).

### Solution
