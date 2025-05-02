How to use?

1. $ source env/bin/activate
2. (env) $ ./findword <word> (e.g., $ ./findword OIECPS)
3. $ SPEC
     SPICE
     SCOPE
     ...
Note! 1. permutated_words.txt is generated which is not important, you can ignore and delete it.
         It contains all of the meaningful and meaningless permutated words contain characters of entry word.
      2. The only dependency for this application is Python pyspellchecker dictionary library which derives
         meaningful words from all of the permutated words inside the permutated_words.txt file.
