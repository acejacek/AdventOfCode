#lang racket

(require 2htdp/batch-io)

(define test-input '("L68" "L30" "R48" "L5" "R60" "L55" "L1" "L99" "R14" "L82"))
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

(display "Part 1: ")
(if (= 3 (process-list test-input 50 0))
    (process-list input 50 0)
    (error "Wrong!"))


(define (process-list-2 lst wheel-pos zero-counter)

  ;(displayln wheel-pos)
  
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
      zero-counter
      (let()
        (define clicks (string->number (substring (car lst) 1)))
        (define (new-counter cl)
          (+ zero-counter (count-zero cl wheel-pos)))
        
        (if (string=? "R" (substring (car lst) 0 1))
          (process-list-2 (cdr lst) (new-wheel-pos clicks) (new-counter clicks))
          (process-list-2 (cdr lst) (new-wheel-pos (- clicks)) (new-counter (- clicks)))))))

(display "Part 2: ")
(if (= 6 (process-list-2 test-input 50 0))
    (process-list-2 input 50 0)
    (error "Wrong!"))
