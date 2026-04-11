# Combined benchmark results

This file aggregates every `*_results_table.csv` under [`results/`](results/).

---

## `results/books_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.000000i_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | lookup_throughput_mops1 | lookup_throughput_mops2 | lookup_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 10205147 | 7987668 | 5489329 | 11825518832 | 334.987 | 334.559 | 326.605 |  |  |
| BTree | 1852413 | 1838879 | 1827622 | 2125000432 | 1.08658 | 1.13937 | 1.14066 | LinearSearch | 6 |
| BTree | 1274699 | 1255606 | 1259722 | 1856251088 | 1.15752 | 1.17601 | 1.16937 | LinearSearch | 8 |
| BTree | 814612 | 807686 | 816719 | 1601106264 | 1.13409 | 1.14401 | 1.16 | InterpolationSearch | 16 |
| DynamicPGM | 4749467 | 4747725 | 4738281 | 1719163668 | 1.72331 | 1.75145 | 1.73616 | BinarySearch | 16 |
| DynamicPGM | 4730379 | 4722950 | 4732110 | 1719163668 | 1.66755 | 1.66735 | 1.63584 | LinearSearch | 16 |
| DynamicPGM | 3541561 | 3526077 | 3527935 | 1703456888 | 1.68243 | 1.68061 | 1.67768 | BinarySearch | 32 |

## `results/books_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.100000i_0m_mix_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | mixed_throughput_mops1 | mixed_throughput_mops2 | mixed_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 10270592 | 7963911 | 5481598 | 11818525760 | 22.3613 | 20.9476 | 20.4186 |  |  |
| BTree | 1445650 | 1431872 | 1275550 | 1956120768 | 1.0052 | 1.01249 | 1.02435 | LinearSearch | 8 |
| BTree | 553106 | 558336 | 547927 | 1881906544 | 0.818018 | 0.819254 | 0.828792 | InterpolationSearch | 10 |
| BTree | 435693 | 435093 | 433253 | 2263536584 | 0.873497 | 0.897328 | 0.900788 | InterpolationSearch | 12 |
| DynamicPGM | 3533146 | 3536493 | 3522446 | 1703429848 | 0.861497 | 0.813178 | 0.846969 | LinearSearch | 32 |
| DynamicPGM | 2777359 | 2771780 | 2772753 | 1700049908 | 0.907073 | 0.897047 | 0.910711 | InterpolationSearch | 128 |
| DynamicPGM | 2743791 | 2744599 | 2739711 | 1700010848 | 0.89745 | 0.89012 | 0.893087 | InterpolationSearch | 256 |

## `results/books_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.500000i_0m_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | insert_throughput_mops1 | lookup_throughput_mops1 | insert_throughput_mops2 | lookup_throughput_mops2 | insert_throughput_mops3 | lookup_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 10127029 | 7966167 | 5510313 | 11785926480 | 2.66751 | 327.541 | 2.27615 | 331.932 | 2.30191 | 333.754 |  |  |
| BTree | 983173 | 981785 | 982727 | 2441636976 | 0.528356 | 0.874551 | 0.531391 | 0.884552 | 0.514225 | 0.882448 | InterpolationSearch | 10 |
| BTree | 1413125 | 878774 | 737988 | 2197517688 | 0.747932 | 0.955377 | 0.693622 | 1.00448 | 0.762348 | 0.994931 | LinearSearch | 8 |
| BTree | 688285 | 684048 | 689747 | 3079164936 | 0.557462 | 1.02243 | 0.556455 | 1.00904 | 0.565986 | 1.03527 | InterpolationSearch | 12 |
| DynamicPGM | 2722689 | 2725842 | 2723378 | 1700010928 | 6.76688 | 0.459365 | 7.32396 | 0.473335 | 7.07302 | 0.469418 | InterpolationSearch | 256 |
| DynamicPGM | 2748743 | 2744713 | 2744752 | 1700049488 | 6.86164 | 0.430446 | 7.01595 | 0.449287 | 6.96742 | 0.450189 | InterpolationSearch | 128 |
| DynamicPGM | 2653244 | 2652917 | 2647015 | 1700003108 | 7.12402 | 0.472141 | 7.12479 | 0.470252 | 7.12076 | 0.469003 | InterpolationSearch | 512 |

## `results/books_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.900000i_0m_mix_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | mixed_throughput_mops1 | mixed_throughput_mops2 | mixed_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 10197388 | 7839977 | 5489798 | 11753613200 | 2.94863 | 2.58685 | 2.64447 |  |  |
| BTree | 1457982 | 1425520 | 1426932 | 2365596448 | 0.736151 | 0.770954 | 0.76207 | LinearSearch | 8 |
| BTree | 736048 | 724232 | 717682 | 2762897224 | 0.617474 | 0.637034 | 0.619797 | InterpolationSearch | 10 |
| BTree | 630863 | 628785 | 617308 | 3159460608 | 0.664601 | 0.644034 | 0.681955 | InterpolationSearch | 12 |
| DynamicPGM | 3447162 | 3446372 | 3453764 | 1703241188 | 2.93062 | 2.99288 | 2.96216 | LinearSearch | 32 |
| DynamicPGM | 2746801 | 2756525 | 2753805 | 1700049408 | 2.8647 | 2.88169 | 2.90174 | InterpolationSearch | 128 |
| DynamicPGM | 2697025 | 2697045 | 2702764 | 1700011168 | 2.93784 | 2.94148 | 2.94267 | InterpolationSearch | 256 |

## `results/fb_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.000000i_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | lookup_throughput_mops1 | lookup_throughput_mops2 | lookup_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 10097465 | 7660837 | 5335485 | 12705922272 | 329.235 | 335.362 | 330.075 |  |  |
| BTree | 1856767 | 1859108 | 1849713 | 2125000432 | 1.08877 | 1.14269 | 1.12811 | LinearSearch | 6 |
| BTree | 1272536 | 1264319 | 1278850 | 1856251088 | 1.15786 | 1.18815 | 1.14503 | LinearSearch | 8 |
| BTree | 1655888 | 1641661 | 1652045 | 2125000432 | 0.969502 | 0.971504 | 0.972938 | InterpolationSearch | 6 |
| DynamicPGM | 5331546 | 5305190 | 5281698 | 1721297388 | 1.60005 | 1.59628 | 1.61263 | LinearSearch | 16 |
| DynamicPGM | 4561499 | 4580701 | 4610923 | 1702563708 | 1.42222 | 1.39543 | 1.40199 | BinarySearch | 128 |
| DynamicPGM | 5346557 | 5334393 | 5324972 | 1721297388 | 1.62369 | 1.61653 | 1.64019 | BinarySearch | 16 |

## `results/fb_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.100000i_0m_mix_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | mixed_throughput_mops1 | mixed_throughput_mops2 | mixed_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 10024640 | 7586583 | 5391953 | 12700946864 | 17.5432 | 15.1751 | 15.9119 |  |  |
| BTree | 1471306 | 1471932 | 1272796 | 1956120768 | 0.976894 | 0.994502 | 1.02664 | LinearSearch | 8 |
| BTree | 563583 | 560841 | 560942 | 1881906544 | 0.733392 | 0.747539 | 0.71637 | InterpolationSearch | 10 |
| BTree | 1132409 | 1160828 | 1136281 | 2197286800 | 0.939325 | 0.973434 | 0.966015 | LinearSearch | 6 |
| DynamicPGM | 4178816 | 4183079 | 4181134 | 1700504528 | 0.776331 | 0.773445 | 0.747214 | BinarySearch | 512 |
| DynamicPGM | 4810795 | 4793729 | 4788857 | 1705226028 | 0.821632 | 0.841953 | 0.846573 | BinarySearch | 64 |
| DynamicPGM | 4568578 | 4580665 | 4581179 | 1702558388 | 0.809388 | 0.81454 | 0.817138 | BinarySearch | 128 |

## `results/fb_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.500000i_0m_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | insert_throughput_mops1 | lookup_throughput_mops1 | insert_throughput_mops2 | lookup_throughput_mops2 | insert_throughput_mops3 | lookup_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 9940529 | 7548061 | 5297008 | 12679095104 | 1.99051 | 333.255 | 1.76108 | 336.646 | 1.73941 | 334.911 |  |  |
| BTree | 1022013 | 1015367 | 1015120 | 2441636976 | 0.492332 | 0.7807 | 0.489899 | 0.776143 | 0.495377 | 0.791348 | InterpolationSearch | 10 |
| BTree | 845108 | 843975 | 840394 | 3079164936 | 0.503137 | 0.866912 | 0.506227 | 0.859448 | 0.50956 | 0.862207 | InterpolationSearch | 12 |
| BTree | 1375821 | 869989 | 766433 | 2197517688 | 0.778862 | 1.03348 | 0.728262 | 0.982922 | 0.749992 | 0.98515 | LinearSearch | 8 |
| DynamicPGM | 4152194 | 4119655 | 4128607 | 1700499248 | 6.76328 | 0.211745 | 7.20164 | 0.213308 | 7.20116 | 0.213048 | LinearSearch | 512 |
| DynamicPGM | 4149641 | 4146152 | 4163768 | 1700499248 | 7.19716 | 0.359335 | 7.23211 | 0.376571 | 7.21411 | 0.369371 | BinarySearch | 512 |
| DynamicPGM | 4386398 | 4378427 | 4353057 | 1701187028 | 7.00865 | 0.323018 | 7.30259 | 0.342845 | 7.30981 | 0.341814 | ExponentialSearch | 256 |

## `results/fb_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.900000i_0m_mix_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | mixed_throughput_mops1 | mixed_throughput_mops2 | mixed_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 9906836 | 7346263 | 5281282 | 12656662928 | 2.16607 | 1.93237 | 1.9234 |  |  |
| BTree | 1463606 | 1479030 | 1474722 | 2365596448 | 0.714324 | 0.739516 | 0.736408 | LinearSearch | 8 |
| BTree | 744358 | 738676 | 741485 | 2762897224 | 0.576326 | 0.570295 | 0.583042 | InterpolationSearch | 10 |
| BTree | 1456228 | 1440113 | 1446582 | 2513462456 | 0.749464 | 0.76767 | 0.766335 | LinearSearch | 6 |
| DynamicPGM | 4117826 | 4116627 | 4122690 | 1700494188 | 2.64588 | 2.72803 | 2.69625 | BinarySearch | 512 |
| DynamicPGM | 4834100 | 4821794 | 4827435 | 1705154448 | 2.88084 | 2.92798 | 2.89415 | BinarySearch | 64 |
| DynamicPGM | 4510820 | 4490880 | 4483651 | 1702518268 | 2.83095 | 2.85845 | 2.84579 | BinarySearch | 128 |

## `results/osmc_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.000000i_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | lookup_throughput_mops1 | lookup_throughput_mops2 | lookup_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 15195532 | 9727778 | 7312091 | 20628848672 | 334.077 | 327.274 | 332.378 |  |  |
| BTree | 1847059 | 1877970 | 1841927 | 2125000432 | 1.38778 | 1.42175 | 1.43787 | LinearSearch | 6 |
| BTree | 1275973 | 1294686 | 1282053 | 1856251088 | 1.39954 | 1.41242 | 1.38063 | LinearSearch | 8 |
| BTree | 854545 | 839685 | 843818 | 1600535632 | 1.12609 | 1.11472 | 1.14458 | BinarySearch | 18 |
| DynamicPGM | 5046792 | 5030714 | 5044756 | 1716194548 | 1.74083 | 1.74415 | 1.7358 | BinarySearch | 16 |
| DynamicPGM | 4724055 | 4717836 | 4715784 | 1707696288 | 1.65991 | 1.65789 | 1.65413 | BinarySearch | 32 |
| DynamicPGM | 5026106 | 5037023 | 5031617 | 1716194548 | 1.7066 | 1.68313 | 1.68468 | LinearSearch | 16 |

## `results/osmc_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.100000i_0m_mix_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | mixed_throughput_mops1 | mixed_throughput_mops2 | mixed_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 15190448 | 9738788 | 7387367 | 20602887232 | 12.9873 | 12.61 | 11.8705 |  |  |
| BTree | 1463263 | 1460646 | 1271994 | 1956120768 | 1.17262 | 1.23358 | 1.21337 | LinearSearch | 8 |
| BTree | 1131742 | 1141926 | 1141505 | 2197286800 | 1.22866 | 1.19974 | 1.21458 | LinearSearch | 6 |
| BTree | 564641 | 562140 | 569456 | 1881906544 | 1.0775 | 1.07187 | 1.09577 | LinearAVX | 10 |
| DynamicPGM | 4407987 | 4407261 | 4383149 | 1700920428 | 0.894711 | 0.906024 | 0.914503 | BinarySearch | 256 |
| DynamicPGM | 4568884 | 4588315 | 4591541 | 1703719788 | 0.939587 | 0.895725 | 0.941876 | BinarySearch | 64 |
| DynamicPGM | 4407941 | 4407417 | 4408062 | 1701834168 | 0.916426 | 0.926805 | 0.926328 | BinarySearch | 128 |

## `results/osmc_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.500000i_0m_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | insert_throughput_mops1 | lookup_throughput_mops1 | insert_throughput_mops2 | lookup_throughput_mops2 | insert_throughput_mops3 | lookup_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 15007055 | 9615747 | 7277797 | 20507817984 | 1.55876 | 330.709 | 1.31997 | 333.363 | 1.38554 | 332.932 |  |  |
| BTree | 1452953 | 1162231 | 1186436 | 2197517688 | 0.701347 | 1.26729 | 0.760085 | 1.31504 | 0.767655 | 1.32015 | LinearSearch | 8 |
| BTree | 948793 | 943114 | 951730 | 2379181072 | 0.712509 | 1.21615 | 0.709364 | 1.148 | 0.684062 | 1.16508 | LinearSearch | 6 |
| BTree | 574862 | 570395 | 564712 | 2441636976 | 0.610019 | 1.12866 | 0.630893 | 1.12493 | 0.606646 | 1.15826 | LinearAVX | 10 |
| DynamicPGM | 4234991 | 4230873 | 4218181 | 1700238628 | 6.08564 | 0.125392 | 6.36896 | 0.126956 | 6.2596 | 0.128335 | LinearSearch | 1024 |
| DynamicPGM | 4231757 | 4232348 | 4233402 | 1700238628 | 6.25842 | 0.396903 | 6.26762 | 0.413614 | 6.25389 | 0.404936 | BinarySearch | 1024 |
| DynamicPGM | 4244166 | 4239465 | 4239020 | 1700238628 | 6.31424 | 0.235085 | 6.32512 | 0.237996 | 6.31699 | 0.241645 | InterpolationSearch | 1024 |

## `results/osmc_100M_public_uint64_ops_2M_0.000000rq_0.500000nl_0.900000i_0m_mix_results_table.csv`

| index_name | build_time_ns1 | build_time_ns2 | build_time_ns3 | index_size_bytes | mixed_throughput_mops1 | mixed_throughput_mops2 | mixed_throughput_mops3 | search_method | value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIPP | 14851204 | 9468549 | 7383968 | 20408967088 | 1.73898 | 1.46834 | 1.47636 |  |  |
| BTree | 1436462 | 1443414 | 1437041 | 2365596448 | 0.744572 | 0.735353 | 0.7466 | LinearSearch | 8 |
| BTree | 1438579 | 1438638 | 1445132 | 2513462456 | 0.757056 | 0.781397 | 0.750121 | LinearSearch | 6 |
| BTree | 745808 | 722980 | 758295 | 2762897224 | 0.64518 | 0.659085 | 0.653805 | LinearAVX | 10 |
| DynamicPGM | 4332449 | 4363651 | 4379852 | 1700923408 | 2.64582 | 2.7071 | 2.67477 | BinarySearch | 256 |
| DynamicPGM | 4497435 | 4496099 | 4497233 | 1703724028 | 2.79971 | 2.77502 | 2.77559 | BinarySearch | 64 |
| DynamicPGM | 4340656 | 4337658 | 4338032 | 1701839508 | 2.75632 | 2.7641 | 2.76644 | BinarySearch | 128 |

