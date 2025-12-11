#lang racket
(require 2htdp/batch-io rackunit)

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

(check-equal? (count-ingredients-1 test-input) 3)
(display "Part 1: ")
(count-ingredients-1 input)

(define (scan-ranges l)  ;full list
  (cond
    [(empty? l) empty]
    [else 
     (define (scan-next rs)
       (if (empty? rs)
           l
           (let* ([r (car rs)]
                  [l-from (car (car l))]
                  [l-to (car (cdr (car l)))]
                  [r-from (car r)]
                  [r-to (car (cdr r))])
             
             (cond
               [(<= l-from r-from r-to l-to) ; r in l
                (cons (list l-from l-to) (scan-ranges
                                          (remove (list l-from l-to)
                                                  (remove (list r-from r-to) l))))]
               [(<= r-from l-from l-to r-to) ; l in r
                (cons (list r-from r-to) (scan-ranges
                                          (remove (list l-from l-to)
                                                  (remove (list r-from r-to) l))))]
               [(<= l-from r-from l-to r-to) ; r overlaps
                (cons (list l-from r-to) (scan-ranges
                                          (remove (list l-from l-to)
                                                  (remove (list r-from r-to)
                                                          l))))]
               [(<= r-from l-from r-to l-to) ; r overlaps  
                (cons (list r-from l-to) (scan-ranges
                                          (remove (list l-from l-to)
                                                  (remove (list r-from r-to)
                                                          l))))]
               
               [else (scan-next (cdr rs))]))))
     
     (scan-next (cdr l))]))

(define (scan-ranges-2 l)
  (if (empty? l)
      empty
      (let ([first-pass (scan-ranges l)])
        (if (empty? first-pass)
            empty
            (cons (car first-pass) (scan-ranges-2 (cdr first-pass)))))))

(define (merge-all ls)
  (let* ([merge-ranges (λ (l) (scan-ranges-2 l))]
         [merged-ls (merge-ranges ls)]
         [merged-again-ls (merge-ranges merged-ls)])
    
    (if (equal? (length merged-ls) (length merged-again-ls))
        merged-ls  ; can't merge any further
        (merge-all merged-again-ls)))) ; merge ranges which overlap


(define (count-ingredients-2 inp)
  (let* 
      ([good-ranges 
        (filter (negate empty?)
                (for/list ([line inp])
                  (if (regexp-match "^[0-9]+-[0-9]+$" line)
                      (map (λ (n) (string->number n)) (regexp-split "-" line))
                      empty)))]
       [reduced-ranges (merge-all good-ranges)])

    (for/sum ([range reduced-ranges])
      (add1 (- (last range) (car range))))))


(check-equal? (count-ingredients-2 test-input) 14)
(display "Part 2: ")
(count-ingredients-2 input)
