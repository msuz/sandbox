# Test Result

```bash
$ python -m unittest discover tests
................................................
----------------------------------------------------------------------
Ran 48 tests in 8.003s

OK
```

```bash
$ python -m unittest tests.test_detail_pages -v
test_generate_urls (tests.test_detail_pages.TestDetailPages) ... ok
test_get_csv_header (tests.test_detail_pages.TestDetailPages) ... ok
test_get_page_text (tests.test_detail_pages.TestDetailPages) ... ok
test_init_urls (tests.test_detail_pages.TestDetailPages) ... ok
test_load (tests.test_detail_pages.TestDetailPages) ... ok
test_load_not_found (tests.test_detail_pages.TestDetailPages) ... ok
test_to_csv (tests.test_detail_pages.TestDetailPages) ... ok

----------------------------------------------------------------------
Ran 7 tests in 3.450s

OK
```

```bash
$ python -m unittest tests.test_kani_page -v
test_parse (tests.test_kani_page.TestKaniPage) ... ok
test_parse_basic_info (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table01 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table02 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table03 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table04 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table05 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table06 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_kani_table07 (tests.test_kani_page.TestKaniPage) ... ok
test_parse_not_found (tests.test_kani_page.TestKaniPage) ... ok
test_parse_radar_chart (tests.test_kani_page.TestKaniPage) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.121s

OK
```

```bash
$ python -m unittest tests.test_feature_page -v

test_parse (tests.test_feature_page.TestFeaturePage) ... ok
test_parse_chartPie (tests.test_feature_page.TestFeaturePage) ... ok
test_parse_chartSeriall (tests.test_feature_page.TestFeaturePage) ... ok
test_parse_legendPiediv_staff (tests.test_feature_page.TestFeaturePage) ... ok
test_parse_legendPiediv_user (tests.test_feature_page.TestFeaturePage) ... ok
test_parse_legendSerialldiv_staff (tests.test_feature_page.TestFeaturePage) ... ok
test_parse_legendSerialldiv_user (tests.test_feature_page.TestFeaturePage) ... ok
test_parse_script_var (tests.test_feature_page.TestFeaturePage) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.030s

OK
```

```bash
$ python -m unittest tests.test_kihon_page -v
test_parse (tests.test_kihon_page.TestKihonPage) ... ok
test_parse_kihon_table01_01 (tests.test_kihon_page.TestKihonPage) ... ok
test_parse_kihon_table01_02 (tests.test_kihon_page.TestKihonPage) ... ok
test_parse_kihon_table02 (tests.test_kihon_page.TestKihonPage) ... ok
test_parse_kihon_table03 (tests.test_kihon_page.TestKihonPage) ... ok
test_parse_kihon_table04 (tests.test_kihon_page.TestKihonPage) ... ok
test_parse_kihon_table05 (tests.test_kihon_page.TestKihonPage) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.331s

OK
```

```bash
$ python -m unittest tests.test_unei_page -v
test_parse (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table01 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table02 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table03 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table04 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table05 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table06 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table07 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table08 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table09 (tests.test_unei_page.TestUneiPage) ... ok
test_parse_checklist_table10 (tests.test_unei_page.TestUneiPage) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.105s

OK
```

```bash
$ python -m unittest tests.test_original_page -v
test_parse (tests.test_original_page.TestOriginalPage) ... ok
test_parse_empty (tests.test_original_page.TestOriginalPage) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.033s

OK
```

```bash
$ python -m unittest tests.test_latestinfo_page -v
test_get (tests.test_latestinfo_page.TestLatestinfoPage) ... ok
test_parse (tests.test_latestinfo_page.TestLatestinfoPage) ... ok

----------------------------------------------------------------------
Ran 2 tests in 3.358s

OK
```
