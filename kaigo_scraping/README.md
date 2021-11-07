# Test Result

```bash
$ python -m unittest -v tests.test_detail_pages
test_generate_urls (tests.test_detail_pages.TestDetailPages) ... ok
test_get_page_text (tests.test_detail_pages.TestDetailPages) ... ok
test_init_urls (tests.test_detail_pages.TestDetailPages) ... ok
test_load (tests.test_detail_pages.TestDetailPages) ... ok
test_to_csv (tests.test_detail_pages.TestDetailPages) ... ok

----------------------------------------------------------------------
Ran 5 tests in 5.103s

OK
```

```bash
$ python -m unittest -v tests.test_kani_page.TestKaniPage
test_parse (tests.test_kani_page.TestKaniPage) ... ok
test_parse_basic_info (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table01 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table02 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table03 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table04 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table05 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table06 (tests.test_kani_page.TestKaniPage) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.092s

OK
```
