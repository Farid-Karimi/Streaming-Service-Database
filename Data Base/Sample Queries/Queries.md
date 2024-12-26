### 1. **Query to Find the Total Payment Amount by Subscription Tier**
This query uses multiple JOINs, aggregate functions, and grouping.

```sql
SELECT 
    s.tier_name, 
    SUM(p.amount) AS total_revenue
FROM 
    subscriptions s
JOIN 
    payments p ON s.subscription_id = p.subscription_id
GROUP BY 
    s.tier_name
ORDER BY 
    total_revenue DESC;
```

**Explanation**:  
- **JOIN**: Combines `subscriptions` and `payments` based on `subscription_id`.  
- **SUM**: Calculates the total payment amount for each tier.  
- **GROUP BY**: Groups results by `tier_name`.  
- **ORDER BY**: Orders the results in descending order of revenue.

---

### 2. **Query to Find Highly Rated Media Produced by Specific Companies**
This query filters data using multiple conditions and involves a JOIN operation.

```sql
SELECT 
    m.title, 
    m.average_rating, 
    pc.name AS production_company
FROM 
    media m
JOIN 
    production_companies pc ON m.production_company_id = pc.company_id
WHERE 
    m.average_rating > 4.5 AND pc.establishment_year < 2000
ORDER BY 
    m.average_rating DESC;
```

**Explanation**:  
- **JOIN**: Connects `media` with `production_companies` using `production_company_id`.  
- **WHERE**: Filters media with a rating higher than 4.5 and production companies established before 2000.  
- **ORDER BY**: Sorts the results by `average_rating` in descending order.

---

### 3. **Query to List Active Subscriptions and Their Expiration Dates**
This query uses filtering conditions with dates.

```sql
SELECT 
    u.username, 
    s.tier_name, 
    s.start_date, 
    s.end_date
FROM 
    subscriptions s
JOIN 
    users u ON s.user_id = u.user_id
WHERE 
    s.end_date > CURRENT_DATE
ORDER BY 
    s.end_date;
```

**Explanation**:  
- **JOIN**: Links `subscriptions` with `users` based on `user_id`.  
- **WHERE**: Filters subscriptions that are still active (`end_date` > `CURRENT_DATE`).  
- **ORDER BY**: Sorts results by `end_date`.

---

### 4. **Query to Find the Most Popular Genres Based on Ratings**
This query involves aggregation and multiple JOINs.

```sql
SELECT 
    m.genre, 
    COUNT(r.rating_id) AS total_ratings, 
    AVG(r.rating_value) AS avg_rating
FROM 
    media m
JOIN 
    ratings r ON m.media_id = r.media_id
GROUP BY 
    m.genre
ORDER BY 
    total_ratings DESC, avg_rating DESC;
```

**Explanation**:  
- **JOIN**: Combines `media` and `ratings` based on `media_id`.  
- **COUNT**: Counts the number of ratings for each genre.  
- **AVG**: Computes the average rating for each genre.  
- **GROUP BY**: Groups data by `genre`.  
- **ORDER BY**: Sorts by popularity (total ratings) and then average rating.

---

### 5. **Query to List Movies with Their Directors and Durations**
This query demonstrates nested JOINs and selected columns.

```sql
SELECT 
    m.title, 
    p.name AS director_name, 
    mv.duration
FROM 
    movies mv
JOIN 
    media m ON mv.media_id = m.media_id
JOIN 
    persons p ON m.director_id = p.person_id
ORDER BY 
    mv.duration DESC;
```

**Explanation**:  
- **JOINs**: Links `movies` with `media` and `persons` tables using `media_id` and `director_id`.  
- **SELECT**: Retrieves the movie title, director name, and duration.  
- **ORDER BY**: Sorts movies by their duration in descending order.
