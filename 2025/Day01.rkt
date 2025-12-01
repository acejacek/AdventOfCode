#lang racket

(require 2htdp/batch-io)

(define test_input '("L68" "L30" "R48" "L5" "R60" "L55" "L1" "L99" "R14" "L82"))
(define input (read-lines "Day01_input.txt"))

(define (process-list lst wheel-pos at-zero-counter)
  
  (define (inc-wheel cl)
    (modulo (+ wheel-pos cl) 100))
  (define (dec-wheel cl)
    (inc-wheel (- cl)))

  (define (at-zero? wheel-pos)
    (if (zero? wheel-pos)
        (+ at-zero-counter 1)
        at-zero-counter))

  ;(displayln wheel-pos)
   
  (if (empty? lst)
      at-zero-counter
      (if (string=? "L" (substring (car lst) 0 1))
          (process-list (cdr lst) (dec-wheel (string->number (substring (car lst) 1))) (at-zero? wheel-pos))
          (process-list (cdr lst) (inc-wheel (string->number (substring (car lst) 1))) (at-zero? wheel-pos)))))

; assert
(if (= 3 (process-list test_input 50 0))
    (process-list input 50 0)
    (error "Wrong!"))


(define (process-list-2 lst wheel-pos at-zero-counter)

  (define (new-wheel-pos cl)
    (modulo (+ wheel-pos cl) 100))

  (define (count-zero clicks pos)
    (define (iter clicks pos counter)
     
      (define (at-zero? pos)
        (if (zero? pos)
            (+ counter 1)
            counter))

      (define (new-pos pos d)
        (modulo (+ pos d) 100))
      
      (cond
        [(< 0 clicks) (iter (- clicks 1) (new-pos pos 1) (at-zero? (new-pos pos 1)))]
        [(> 0 clicks) (iter (+ clicks 1) (new-pos pos (- 1)) (at-zero? (new-pos pos (- 1))))]
        [else counter]))
          
    (iter clicks pos 0))

  (if (empty? lst)
      at-zero-counter
      (let()
        (define clicks (string->number (substring (car lst) 1)))
        (if (string=? "L" (substring (car lst) 0 1))
          (process-list-2 (cdr lst) (new-wheel-pos clicks) (count-zero clicks wheel-pos))
          (process-list-2 (cdr lst) (new-wheel-pos (- clicks)) (count-zero (- clicks) wheel-pos))))))

; assert

(define part-2 (process-list-2 test_input 50 0))
(if (= 6 part-2)
    (process-list-2 input 50 0)
    (error (number->string part-2)))
