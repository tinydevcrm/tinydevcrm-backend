# IEEE Software Requirements Specification Template

Copyright 2020-Present Ying Wang

This document serves as a [living
document](https://en.wikipedia.org/wiki/Living_document) for TinyDevCRM's system
design, tradeoffs, and otherwise considerations. It complies with [IEEE Standard
830-1998](IEEE-Std-830-1998.pdf) defined best practices.

__________

## Software Requirements Specification

for TinyDevCRM

Version MVP

TinyDevCRM / Ying Wang

June 5th, 2020

__________

## Table of Contents

__________

## Revision History

Name | Date | Reason For Changes | Version
--- | --- | --- | ---
Ying Wang | 06/05/2020 | Initial definition | MVP

__________

## 1. Introduction

### 1.1 Purpose

TinyDevCRM evolved in purpose from a CRM (customer relationship management)
platform for software engineers, to a general data layer for event-driven
clients, to what may be best described as a hybrid OLTP/OLAP platform enabling
streaming "business intelligence"-like purposes. TinyDevCRM serves as the
one-stop data lake for personal apps and side projects.

The scope of the project covered in this specific document includes the Django
web application backend, the PostgreSQL data model, and the Pushpin realtime API
reverse proxy.

This document does not currently cover any graphical user interfaces (GUIs),
connectors or adaptors, deep dives into dependencies, or deployment models.
Documentation on those sections should be covered by their respective
respositories, or relocated to a separate repository in the near future.

### 1.2 Document Conventions

*Describe any standards or typographical conventions that were followed when
writing this SRS, such as fonts or highlighting that have special significance.
For example, state whether priorities for higher-level requirements are assumed
to be inherited by detailed requirements, or whether every requirement statement
is to have its own priority.*

### 1.3 Intended Audience and Reading Suggestions

This document is intended for me (my future self) when coming back to this
project to make additional modifications and consider additional tradeoffs, in
order to ground the purpose of the project and inform future actionables and
deliverables.

This document may be read and understood by other technical users looking to
contribute or fork this project for their own personal needs. This document is
not intended as a user guide or a how-to guide.

Reading through the guide from top to bottom should be fine for understanding
all the content contained here.

### 1.4 Product Scope

*Provide a short description of the software being specified and its purpose,
including relevant benefits, objectives, and goals. Relate the software to
corporate goals or business strategies. If a separate vision and scope document
is available, refer to it rather than duplicating its contents here.*

### 1.5 References

*List any other documents or Web addresses to which this SRS refers. These may
include user interface style guides, contracts, standards, system requirements
specifications, use case documents, or a vision and scope document. Provide
enough information so that the reader could access a copy of each reference,
including title, author, version number, date, and source or location.*

__________

## 2. Overall Description

### 2.1 Product Perspective

*Describe the context and origin of the product being specified in this SRS. For
example, state whether this product is a follow-on member of a product family, a
replacement for certain existing systems, or a new, self-contained product. If
the SRS defines a component of a larger system, relate the requirements of the
larger system to the functionality of this software and identify interfaces
between the two. A simple diagram that shows the major components of the overall
system, subsystem interconnections, and external interfaces can be helpful.*

### 2.2 Product Functions

*Summarize the major functions the product must perform or must let the user
perform. Details will be provided in Section 3, so only a high level summary
(such as a bullet list) is needed here. Organize the functions to make them
understandable to any reader of the SRS. A picture of the major groups of
related requirements and how they relate, such as a top level data flow diagram
or object class diagram, is often effective.*

### 2.3 User Classes and Characteristics

*Identify the various user classes that you anticipate will use this product.
User classes may be differentiated based on frequency of use, subset of product
functions used, technical expertise, security or privilege levels, educational
level, or experience. Describe the pertinent characteristics of each user class.
Certain requirements may pertain only to certain user classes. Distinguish the
most important user classes for this product from those who are less important
to satisfy.*

### 2.4 Operating Environment

*Describe the environment in which the software will operate, including the
hardware platform, operating system and versions, and any other software
components or applications with which it must peacefully coexist.*

### 2.5 Digital and Implementation Constraints

*Describe any items or issues that will limit the options available to the
developers. These might include: corporate or regulatory policies; hardware
limitations (timing requirements, memory requirements); interfaces to other
applications; specific technologies, tools, and databases to be used; parallel
operations; language requirements; communications protocols; security
considerations; design conventions or programming standards (for example, if the
customer’s organization will be responsible for maintaining the delivered
software).*

### 2.6 User Documentation

*List the user documentation components (such as user manuals, on-line help, and
tutorials) that will be delivered along with the software. Identify any known
user documentation delivery formats or standards.*

### 2.7 Assumptions and Dependencies

*List any assumed factors (as opposed to known facts) that could affect the
requirements stated in the SRS. These could include third-party or commercial
components that you plan to use, issues around the development or operating
environment, or constraints. The project could be affected if these assumptions
are incorrect, are not shared, or change. Also identify any dependencies the
project has on external factors, such as software components that you intend to
reuse from another project, unless they are already documented elsewhere (for
example, in the vision and scope document or the project plan).*

__________

## 3. External Interface Requirements

### 3.1 User Interfaces

*Describe the logical characteristics of each interface between the software
product and the users. This may include sample screen images, any GUI standards
or product family style guides that are to be followed, screen layout
constraints, standard buttons and functions (e.g., help) that will appear on
every screen, keyboard shortcuts, error message display standards, and so on.
Define the software components for which a user interface is needed. Details of
the user interface design should be documented in a separate user interface
specification.*

### 3.2 Hardware Interfaces

*Describe the logical and physical characteristics of each interface between the
software product and the hardware components of the system. This may include the
supported device types, the nature of the data and control interactions between
the software and the hardware, and communication protocols to be used.*

### 3.3 Software Interfaces

*Describe the connections between this product and other specific software
components (name and version), including databases, operating systems, tools,
libraries, and integrated commercial components. Identify the data items or
messages coming into the system and going out and describe the purpose of each.
Describe the services needed and the nature of communications. Refer to
documents that describe detailed application programming interface protocols.
Identify data that will be shared across software components. If the data
sharing mechanism must be implemented in a specific way (for example, use of a
global data area in a multitasking operating system), specify this as an
implementation constraint.*

### 3.4 Communications Interfaces

*Describe the requirements associated with any communications functions required
by this product, including e-mail, web browser, network server communications
protocols, electronic forms, and so on. Define any pertinent message formatting.
Identify any communication standards that will be used, such as FTP or HTTP.
Specify any communication security or encryption issues, data transfer rates,
and synchronization mechanisms.*

__________

## 4. System Features

*This template illustrates organizing the functional requirements for the
product by system features, the major services provided by the product. You may
prefer to organize this section by use case, mode of operation, user class,
object class, functional hierarchy, or combinations of these, whatever makes the
most logical sense for your product.*

### 4.1 System Feature 1

*Don’t really say “System Feature 1.” State the feature name in just a few
words.*

#### 4.1.1 Description and Priority

*Provide a short description of the feature and indicate whether it is of High,
Medium, or Low priority. You could also include specific priority component
ratings, such as benefit, penalty, cost, and risk (each rated on a relative
scale from a low of 1 to a high of 9).*

#### 4.1.2 Stimulus / Response Sequences

*List the sequences of user actions and system responses that stimulate the
behavior defined for this feature. These will correspond to the dialog elements
associated with use cases.*

#### 4.1.3 Functional Requirements

*Itemize the detailed functional requirements associated with this feature.
These are the software capabilities that must be present in order for the user
to carry out the services provided by the feature, or to execute the use case.
Include how the product should respond to anticipated error conditions or
invalid inputs. Requirements should be concise, complete, unambiguous,
verifiable, and necessary. Use “TBD” as a placeholder to indicate when necessary
information is not yet available.*

*Each requirement should be uniquely identified with a sequence number or a
meaningful tag of some kind.*

REQ-1:

REQ-2:


### 4.2 User Creation

#### 4.2.1 Description and Priority

#### 4.2.2 Stimulus / Response Sequences

#### 4.2.3 Functional Requirements

#### 4.2.4 System Design Alternatives / Tradeoffs / Considerations


### 4.2 Data Import

#### 4.2.1 Description and Priority

#### 4.2.2 Stimulus / Response Sequences

#### 4.2.3 Functional Requirements

#### 4.2.4 System Design Alternatives / Tradeoffs / Considerations




### 4.2 Table Definitions

#### 4.2.1 Description and Priority

#### 4.2.2 Stimulus / Response Sequences

#### 4.2.3 Functional Requirements

#### 4.2.4 System Design Alternatives / Tradeoffs / Considerations



### 4.2 Materialized Views

#### 4.2.1 Description and Priority

TinyDevCRM can define materialized views on a user's tables using an arbitrary
read-only SQL statement passed-through an HTTP POST request. The limitations of
this SQL statement is it cannot be comprised of multiple SQL statements (i.e. no
semicolons), and must begin with a `SELECT`, `TABLES`, or `VALUES` query to
enforce read-only status.

The benefit of creating a materialized view is caching a specific query within
PostgreSQL, while referencing the same underlying data. This way, different
requesters have access to the same source of truth.

#### 4.2.2 Stimulus / Response Sequences

#### 4.2.3 Functional Requirements

#### 4.2.4 System Design Alternatives / Tradeoffs / Considerations



### 4.2 Cron Job Definitions

#### 4.2.1 Description and Priority

TinyDevCRM runs cron jobs in order to manage lifecycles of different PostgreSQL
tables and views. Currently, cron jobs can be run in order to refresh a specific
materialized view,

#### 4.2.2 Stimulus / Response Sequences

#### 4.2.3 Functional Requirements

#### 4.2.4 System Design Alternatives / Tradeoffs / Considerations

One alternative to `pg_cron` is to run `cron` apart from having a special
PostgreSQL extension. One way to do this would be to set up a Docker container
with `cron` running as the foreground process, in order to issue events to a
separate server. This would be far easier to set up using a vanilla
database and a compute layer, and translates better to cloud-native
infrastructure. However the system design may force a possibility of network
faults (cloud infrastructure is completely virtualized, but on-premises may not
be) and separate management overhead (e.g. database compute goes down, cron
actions ineffectual).

Another alternative to `pg_cron` would be to run AWS CloudWatch and use AWS
Lambda in a serverless fashion to poll the database and refresh materialized
views. AWS Lambda does offer 1 million free function calls as part of its free
tier. However, AWS Lambda requires maintaining an entire runtime that needs to
be migrated per runtime upgrade, is difficult to version especially with AWS
CloudFormation, and needs to interface with other AWS services in order to run.
More importantly, it is native to AWS and cannot be migrated to another cloud
provider or to an on-premises deployment without changing source code. Last,
refreshes on a per-minute granularity would only allow ~25 materialized views to
be refreshed before running into billing concerns, or before materialized views
must be chained together.

### 4.2 Realtime Streaming

#### 4.2.1 Description and Priority

#### 4.2.2 Stimulus / Response Sequences

#### 4.2.3 Functional Requirements

#### 4.2.4 System Design Alternatives / Tradeoffs / Considerations

This service uses HTTP/2 and [Server-Sent
Events](https://en.wikipedia.org/wiki/Server-sent_events). The living
specification for Server-Sent Events as of this writing can be found on [the
HTML specification
page](https://html.spec.whatwg.org/multipage/server-sent-events.html).
Server-Sent events are unidirectional (data flows from server to client), uses
HTTP for better compliance with existing infrastructure (pass-through packet
inspection, no SDK required), and supports automatic event playback in case a
connection is dropped. Disadvantages of SSE, such as UTF-8 support only,
connection limits per browser, and lower popularity than WebSockets, don't
currently outweigh the perceived benefits.

Other alternatives to Server-Sent Events include WebSockets and HTTP
long-polling, although it remains unlikely Server-Sent Events will be deprecated
since it is integrated into the HTML standard. If channel limits occur, update
the Django model to listen to multiple jobs per channel.

### 4.3 Realtime Reverse Proxies

#### 4.3.4 System Design Alternatives / Tradeoffs / Considerations

This service uses [Pushpin](https://github.com/fanout/pushpin), a reverse proxy
specifically designed for realtime APIs. Pushpin is fully open-source, has
plenty of connectors, has a managed cloud CDN solution available, and leverages
an open-source, underlying internal protocol called "GRIP".

One alternative to Pushpin include [`nchan`](https://nchan.io/), which is
currently an NGINX extensions module supporting realtime streaming needs. While
this may have made deployments much easier had I used NGINX in production,
discussions with the `nchan` maintainer indicates the NGINX API isn't designed
for realtime needs, which results in issues such as memory leaks. `nchan` is
currently undergoing a rewrite into a separate server, and if Pushpin no longer
suits TinyDevCRM's requirements, `nchan` should be re-considered for usage at
that time.

Another alternative to Pushpin is [`envoy`](https://www.envoyproxy.io/), which
is an enterprise-grade reverse proxy for cloud-native applications. Looking at
the documentation indicates far more complexity than is necessary for
TinyDevCRM's needs, and as TinyDevCRM's purpose is to eventually move off of the
cloud and onto on-premise compute instances for long-term usage, Envoy doesn't
look like the right fit for this project. Look at this project if a fork of
TinyDevCRM for enterprise-grade use cases is ever commercially viable.

### 4.4 Message brokering / message queueing

#### 4.2.1 Description and Priority

#### 4.2.2 Stimulus / Response Sequences

#### 4.2.3 Functional Requirements

#### 4.4.4 System Design Alternatives / Tradeoffs / Considerations

TinyDevCRM does not use an explicit message queue. Instead, messages are
automatically queued using the PostgreSQL databasae as the underlying backing
store, using `django_eventstream` and the setting
`settings.EVENTSTREAM_STORAGE_CLASS`. This ensures events have the ability to
suspend-to-disk in addition to suspend-to-RAM, which may be cheaper (if disk vs.
RAM costs are passed to the consumer), and more secure (since disk can be
encrypted).

Correspondingly, TinyDevCRM also does not use an off-the-shelf message broker.
Instead, a custom Python script, `broker.py`, uses `psycopg2`'s advanced
[asynchronous
notifications](https://www.psycopg.org/docs/advanced.html#asynchronous-notifications)
feature in order to listen to a specific channel, fetch text-based payloads sent
on that channel, converts it into JSON, translates that JSON into a package sent
out on the correct channel. This arrangement limits the amount of "magic" that
goes into message brokering, is easy to debug and troubleshoot (run as a
separate Docker container and examine logs printed to stdout), easy to scale
(since the broker is fronted with a custom `django-admin` command, it can be
Dockerized and run as a standalone container), and performant enough given a
light load.

If load requirements become an issue in production, Pushpin supports ZeroMQ
pub/sub for client connections to push directly to the end-user channel. A
ZeroMQ client can be installed on the PostgreSQL database instance, and a
foreign data wrapper / stored procedure templates written and installed to push
PostgreSQL events onto a ZeroMQ channel for publishing to Pushpin. This means
the web application backend only needs to orchestrate channel setup and
teardown, and that the database and reverse proxy can scale independently to
handle increased load.

Popular message brokers / message queue solutions for Python-based web
application needs include RabbitMQ, Celery, and Redis. I did not choose these
solutions since they would cause dependency bloat and maintenance overhead in
the future, and since I already had a backing store and the ability to create
simple top-level orchestration processes already. If scaling issues prove more
difficult than configuring additional channels (and migrating other users to
separate TinyDevCRM instances), re-consider using these solutions.

__________

## 5. Other Nonfunctional Requirements

### 5.1 Performance Requirements

*If there are performance requirements for the product under various
circumstances, state them here and explain their rationale, to help the
developers understand the intent and make suitable design choices. Specify the
timing relationships for real time systems. Make such requirements as specific
as possible. You may need to state performance requirements for individual
functional requirements or features.*

### 5.2 Safety Requirements

*Specify those requirements that are concerned with possible loss, damage, or
harm that could result from the use of the product. Define any safeguards or
actions that must be taken, as well as actions that must be prevented. Refer to
any external policies or regulations that state safety issues that affect the
product’s design or use. Define any safety certifications that must be
satisfied.*

### 5.3 Security Requirements

*Specify any requirements regarding security or privacy issues surrounding use
of the product or protection of the data used or created by the product. Define
any user identity authentication requirements. Refer to any external policies or
regulations containing security issues that affect the product. Define any
security or privacy certifications that must be satisfied.*

### 5.4 Software Quality Attributes

*Specify any additional quality characteristics for the product that will be
important to either the customers or the developers. Some to consider are:
adaptability, availability, correctness, flexibility, interoperability,
maintainability, portability, reliability, reusability, robustness, testability,
and usability. Write these to be specific, quantitative, and verifiable when
possible. At the least, clarify the relative preferences for various attributes,
such as ease of use over ease of learning.*

### 5.5 Business Rules

*List any operating principles about the product, such as which individuals or
roles can perform which functions under specific circumstances. These are not
functional requirements in themselves, but they may imply certain functional
requirements to enforce the rules.*

__________

## 6. Other Requirements

*Define any other requirements not covered elsewhere in the SRS. This might
include database requirements, internationalization requirements, legal
requirements, reuse objectives for the project, and so on. Add any new sections
that are pertinent to the project.*

__________

## Appendix A: Glossary

*Define all the terms necessary to properly interpret the SRS, including
acronyms and abbreviations. You may wish to build a separate glossary that spans
multiple projects or the entire organization, and just include terms specific to
a single project in each SRS.*

__________

## Appendix B: Analysis Models

*Optionally, include any pertinent analysis models, such as data flow diagrams,
class diagrams, state-transition diagrams, or entity-relationship diagrams.*

__________

## Appendix C: To Be Determined List

*Collect a numbered list of the TBD (to be determined) references that remain in
the SRS so they can be tracked to closure.*
