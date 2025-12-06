#lang racket

(require 2htdp/batch-io)

(define test (list 
  "987654321111111"
  "811111111111119"
  "234234234234278"
  "818181911112111"))

(define input (read-lines "Day03_input.txt"))

(define (max-element x y) (if (> x y) x y))

;max element in list
(define (max-list ls)
    (if (null? (cdr ls))
        (car ls)
        (max-element (car ls) (max-list (cdr ls)))))

(define (index-of li element) ; search for index of element in list li
  (let loop ([lst li]
             [idx 0])
    (cond
      [(equal? (first lst) element) idx]
      [else (loop (rest lst) (add1 idx))])))

; builds a list of digits of expected length
(define (build-max ls expect)
  (cond
    [(< expect 1) empty]
    [(empty? ls) empty]
    [(let*
         ([max-element (max-list ls)]
          [max-idx (index-of ls max-element)]
          [l-ls (take ls max-idx)]
          [r-ls (if (< max-idx (length ls))
                    (drop ls (add1 max-idx))
                    empty)])
       (append
        (build-max l-ls (- expect (length r-ls) 1))
        (list max-element)
        (build-max r-ls (- expect 1))))]))

; converts '(1 3 8 2) to 1382
(define (calculate-number lst)
  (let loop ([ls (reverse lst)]
             [number 0]
             [exp 0])
    (if (empty? ls)
        number
        (loop (cdr ls)
              (+ number (* (car ls) (expt 10 exp)))
              (add1 exp)))))

(define (max-joltage banks len)
  (for/fold ([joltage 0])
            ([bank banks])
    (let*
      ([list-of-numbers (map (λ(n) (- n 48)) (map char->integer (string->list bank)))]
       [bank-joltage (calculate-number (build-max list-of-numbers len))])
      (+ joltage bank-joltage))))

(display "Part 1: ")
(if (= 357 (max-joltage test 2))
    (max-joltage input 2)
    (error "wrong result"))

(display "Part 2: ")
(if (= 3121910778619 (max-joltage test 12))
    (max-joltage input 12)
    (error "wrong result"))