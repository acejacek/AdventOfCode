#lang racket

(define test-input '("11-22" "95-115" "998-1012" "1188511880-1188511890" "222220-222224" 
"1698522-1698528" "446443-446449" "38593856-38593862" "565653-565659" 
"824824821-824824827" "2121212118-2121212124"))

(define from (string->number (car (string-split "11-22" "-"))))
(define to (string->number(car(cdr (string-split "11-22" "-")))))

(struct range (from to))

(define r (range from to))

;(range-from r)
;(range-to r)

(define (generate start end)
  
  (define (iter start end result)
    (define (len number) (string-length (number->string number)))
    (define (divisor len)
      (expt 10 (quotient len 2)))
    (define left (quotient start (divisor (len start))))
    (define right (modulo start (divisor (len start))))
    
    (cond
      [(> start end) result]
      [else
       (if (= left right)
           (iter (add1 start) end (+ result start))
           (iter (add1 start) end result))]))
  (iter start end 0))

(generate (range-from r) (range-to r))

(define (process list)
  (define (iterate list sum)
    (if (empty? list)
        sum
        (let()
          (define from (string->number (car (string-split (car list) "-"))))
          (define to (string->number(car(cdr (string-split (car list) "-")))))
          (struct range (from to))
          (define r (range from to))
          (iterate (cdr list) (+ sum (generate (range-from r) (range-to r)))))))
  (iterate list 0))

(process test-input)
