-- QUERY 1: Count total books
SELECT COUNT(*) AS total_books
FROM Books;


-- QUERY 2: WHERE - Books that are in stock
SELECT title, price_inr, rating
FROM Books
WHERE availability = 1;


-- QUERY 3: ORDER BY and LIMIT - Top 10 expensive books
SELECT title, price_inr
FROM Books
ORDER BY price_inr DESC
LIMIT 10;


-- QUERY 4: DISTINCT - List all unique categories
SELECT DISTINCT category_name
FROM Categories;


-- QUERY 5: IN - Books belonging to selected categories
SELECT b.title, c.category_name, b.rating
FROM Books b
JOIN Categories c
ON b.category_id = c.category_id
WHERE c.category_name IN ('Travel', 'Mystery');


-- QUERY 6: BETWEEN - Books priced between ₹500 and ₹1500
SELECT title, price_inr
FROM Books
WHERE price_inr BETWEEN 500 AND 1500
ORDER BY price_inr;


-- QUERY 7: JOIN - Average price and book count per category
SELECT
    c.category_name,
    COUNT(b.book_id) AS total_books,
    ROUND(AVG(b.price_inr), 2) AS average_price_inr
FROM Categories c
JOIN Books b
ON c.category_id = b.category_id
GROUP BY c.category_name
ORDER BY average_price_inr DESC;


-- QUERY 8: Ratings summary per category
SELECT
    c.category_name,
    AVG(b.rating) AS average_rating
FROM Books b
JOIN Categories c
ON b.category_id = c.category_id
GROUP BY c.category_name;
