# Database Design & Implementation for a Streaming Service Platform

## Project Overview
For this project, I designed and implemented a database system tailored for a streaming service platform. The goal was to create a structure that could effectively handle users, media content, subscriptions, payments, and more. The work was split into two main phases: **Database Design and Analysis** and **Implementation and Optimization**.


## Phase 1: Database Design and Analysis
This phase was all about sketching out the structure and relationships of the database. I created both **Enhanced Entity-Relationship (EER)** and **UML-style diagrams**, which are available in the [diagrams folder](https://github.com/Farid-Karimi/DB-Project/tree/master/Diagrams). To make it even more accessible, I also used [dbdiagram.io](https://dbdiagram.io/d/DB-Bonus-Project-phase-one-674b7223e9daa85aca3b9a09) to write the schema in DBML.

### Entity-Relationship Model
The database schema revolves around a mix of core, support, and interaction entities:  
- **Core Entities**:  
  - Users  
  - Media (Movies and Series)  
  - Subscriptions  

- **Support Entities**:  
  - Payment  
  - Episodes  
  - Storage Location  
  - Production Company  

- **Interaction Entities**:  
  - Comments  
  - Ratings  
  - WatchLaterLists  

### Key Relationships
Here’s how everything connects:  
- Users can have multiple subscriptions and interact with media by commenting and rating.  
- Media content is organized hierarchically—movies, series, and episodes.  
- Production companies and storage locations are linked to media, making the backend more manageable.  

### Constraints
I added a few rules to make sure the data stays clean and functional:  
- **Validation**: Ratings are limited to a 0-5 scale.  
- **Uniqueness**: User emails and media titles must be unique.  
- **Integrity**: Foreign keys enforce relationships between entities.  
- **No Duplicate Ratings**: A user can’t rate the same media more than once.  

---

## Phase 2: Implementation and Optimization
In this phase, I turned the design into a fully functional database. You can check out the **DDL SQL code** [here](https://github.com/Farid-Karimi/DB-Project/tree/master/Data%20Base/DDL%20Code), and the final **ERD diagrams** are in the [diagrams folder](https://github.com/Farid-Karimi/DB-Project/tree/master/Diagrams).

To test the database, I used Python and the **Faker library** to generate synthetic data. All the scripts and dependencies are available in the [code folder](https://github.com/Farid-Karimi/DB-Project/tree/master/Code). I also wrote sample SQL queries and documented the results with screenshots in the [Sample Queries folder](https://github.com/Farid-Karimi/DB-Project/tree/master/Data%20Base/Sample%20Queries).  

### Database Normalization
I optimized the database by applying **Second Normal Form (2NF)**.  
Here are a couple of key improvements:  
- **Partial Dependency Fix**: In the Episodes table, storage-related attributes like `storage_server` and `storage_path` were moved out since they depended on the `series_id` instead of the `episode_id`.  
- **Profile Picture Optimization**: Instead of storing images as BLOBs, I used path-based references. This allows users to upload higher-quality images without bloating the database.  

### Technical Implementation
Here’s the tech stack and tools I used:  
- **Database Platform**: PostgreSQL  
- **Development Environment**: PyCharm  
- **Data Generation**: Faker library (super handy for creating realistic sample data)  

### Database Features
The final database has a lot going for it:  
- User management with unique profiles and subscriptions.  
- Organized media content with hierarchy (movies, series, episodes).  
- Subscription tracking and payment history.  
- User interaction features like comments, ratings, and watch lists.  
- Efficient storage management for media and user assets.  

---

### Final Thoughts
This project provided an in-depth exploration of designing and implementing a scalable database system for a modern streaming platform. While I had ambitious plans to create a desktop application or a web app to fully utilize the database's capabilities, time constraints—being a final project—prevented me from pursuing this additional step. However, I see this as an opportunity for future improvements and development!
