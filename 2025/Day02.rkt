#lang racket

(define test-input '("11-22" "95-115" "998-1012" "1188511880-1188511890" "222220-222224" 
"1698522-1698528" "446443-446449" "38593856-38593862" "565653-565659" 
"824824821-824824827" "2121212118-2121212124"))

(define input (string-split (car (file->lines "Day02_input.txt")) ","))

(define (process-1 list)
  
  (define (generate start end)
    (define (iter start end result)
      (define len
        (λ (n) (string-length (number->string n))))
      (define divisor
        (λ (l) (expt 10 (quotient l 2))))
      (define left (quotient start (divisor (len start))))
      (define right (modulo start (divisor (len start))))
    
      (cond
        [(> start end) result]
        [(= left right) (iter (add1 start) end (+ result start))]
        [else (iter (add1 start) end result)]))
    (iter start end 0))
  
  (define (iterate list sum)
    (if (empty? list)
        sum
        (let()
          (define from (string->number (car (string-split (car list) "-"))))
          (define to (string->number(car (cdr (string-split (car list) "-")))))
          (iterate (cdr list) (+ sum (generate from to))))))
  (iterate list 0))

(display "Part 1: ")
(if (= 1227775554 (process-1 test-input))
    (process-1 input)
    (error "Wrong"))

(define (process-2 list)
  
  (define (invalid-id? test-number)
    (define (iterate-options n)
      (define len
        (λ (n) (string-length (number->string n))))
      (define half
        (λ (l) (quotient (len l) 2)))
      (define (match-this pattern)
        (begin
          (define multiplier (quotient (len test-number) (string-length pattern)))
          (define expr (string-append "^(" pattern "){" (number->string multiplier) "}$"))
          (regexp-match-exact? (pregexp expr) (number->string test-number))))
      (cond
        [(zero? n) #f]
        [(and (even? (len n)) (match-this (substring (number->string test-number) 0 (half n)))) #t]
        [else (iterate-options (quotient n 10))]))

    (iterate-options test-number))
  
  (define (find-invalid list-of-n)
    (for/fold ([result 0])
              ([number list-of-n]
               #:when (invalid-id? number))
      (+ result number)))
  
  (define (iterate list)
    (for/fold ([sum 0])
              ([element list])
       (let()
         (define from (string->number (car (string-split element "-"))))
         (define to (string->number(car (cdr (string-split element "-")))))
         (+ sum (find-invalid (range from (add1 to)))))))

  (iterate list))

(display "Part 2: ")
(if (= 4174379265 (process-2 test-input))
    (process-2 input)
    (error "Wrong"))
