#lang racket

(define test (list 
  "818181911112111"
  "987654321111111"
  "811111111111119"
  "234234234234278"
  "818181911112111"))

(define (list-of-numbers number)
  (map (λ(n) (- n 48)) (map char->integer (string->list number))))

(define list (list-of-numbers test))


(define (max-element x y) (if (> x y) x y))

(define (max-list ls)
    (if (null? (cdr ls))
        (car ls)
        (max-element (car ls) (max-list (cdr ls)))))

(define max-element-1 (max-list list))

(define (index-of list element)
  (let loop ([lst list]
             [idx 0])
    (cond
      [(empty? lst) #f]
      [(equal? (first lst) element) idx]
      [else (loop (rest lst) (add1 idx))])))

(define max-1-idx (index-of list max-element-1))
(define right-list (drop list (add1 max-1-idx)))

(if (empty? right-list)
      (+ max-element-1 (* 10 (max-list (take list max-1-idx))))
      (+ (* 10 max-element-1) (max-list right-list)))

(define (max-joltage list)
  
  (for/fold ([joltage 0])
            ([bank list])
    (let()
      (define (list-of-numbers number)
        (map (λ(n) (- n 48)) (map char->integer (string->list bank))))
      (define list (list-of-numbers test))
      
    ))