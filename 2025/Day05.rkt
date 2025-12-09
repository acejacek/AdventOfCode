#lang racket
(require 2htdp/batch-io)

(define test-input (list
                    "3-5"
                    "10-14"
                    "16-20"
                    "12-18"
                    ""
                    "1"
                    "5"
                    "8"
                    "11"
                    "17"
                    "32"))

(define input (read-lines "Day05_input.txt"))

(define (good-ranges lst)
  (filter (negate empty?)
          (for/list ([line lst])
            (if (regexp-match "^[0-9]+-[0-9]+$" line)
                (map (λ (n) (string->number n)) (regexp-split "-" line))
                empty))))

(define (ingredients lst)
  (filter (negate empty?)
          (for/list ([line lst])
            (if (regexp-match "^[0-9]+$" line)
                (string->number line)
                empty))))

(define (count-ingredients-1 inp)
  (let* 
      ([good-ranges 
        (filter (negate empty?)
                (for/list ([line inp])
                  (if (regexp-match "^[0-9]+-[0-9]+$" line)
                      (map (λ (n) (string->number n)) (regexp-split "-" line))
                      empty)))]
       [ingredients
        (filter (negate empty?)
                (for/list ([line inp])
                  (if (regexp-match "^[0-9]+$" line)
                      (string->number line)
                      empty)))])
    
    (foldl (λ (n result)
             (+ result
                (let check ([ran good-ranges])
                  (cond
                    [(empty? ran) 0]
                    [(<= (list-ref (car ran) 0) n (list-ref (car ran) 1)) 1]
                    [else (check (cdr ran))]))))
           0
           ingredients)))

; out of mem, obviously
(define (count-ingredients-2-naive inp)
  (let* 
      ([good-ranges 
        (filter (negate empty?)
                (for/list ([line inp])
                  (if (regexp-match "^[0-9]+-[0-9]+$" line)
                      (map (λ (n) (string->number n)) (regexp-split "-" line))
                      empty)))])

    (length
     (remove-duplicates
      (flatten
       (for/list ([ran good-ranges])
         (stream->list
          (in-inclusive-range (car ran) (car (cdr ran))))))))))


       
(if (= 3 (count-ingredients-1 test-input))
    (count-ingredients-1 input)
    (error "wrong"))

;(if (= 14 (count-ingredients-2 test-input))
;    (count-ingredients-2 input)
;    (error "wrong"))
