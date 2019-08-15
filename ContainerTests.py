import time
from Container import Container

if __name__ == "__main__":
    print("TEST CASE 1 ##############################")
    a = Container(length=5, width=2, height=5, boxes=[{"length": 5, "height": 5, "width": 5}])
    assert not a.placeBoxesSequentially()
    print("")

    print("TEST CASE 2 ##############################")
    b = Container(length=5, width=5, height=3, boxes=[{"length": 5, "height": 5, "width": 5}])
    assert not b.placeBoxesSequentially()
    print("")

    print("TEST CASE 3 ##############################")
    c = Container(length=5, width=5, height=5, boxes=[{"length": 5, "height": 5, "width": 5}])
    assert c.placeBoxesSequentially()
    print("")

    print("TEST CASE 4 ##############################")
    d = Container(length=5, width=10, height=5, boxes=[{"length": 5, "height": 5, "width": 5}, {"length": 5, "height": 5, "width": 5}])
    assert d.placeBoxesSequentially()
    print("")

    print("TEST CASE 5 ##############################")
    e = Container(length=5, width=5, height=10,
                  boxes=[{"length": 5, "height": 5, "width": 5}, {"length": 5, "height": 5, "width": 5}])
    assert e.placeBoxesSequentially()
    print("")

    print("TEST CASE 6 ##############################")
    # one box is too wide 7 vs 5
    f = Container(length=5, width=5, height=18,
                  boxes=[{"length": 5, "height": 5, "width": 5}, {"length": 4, "height": 6, "width": 4},
                         {"length": 5, "height": 4, "width": 7}])
    assert not f.placeBoxesSequentially()
    print("")

    print("TEST CASE 7 ##############################")
    g = Container(length=5, width=5, height=18,
                  boxes=[{"length": 5, "height": 5, "width": 5}, {"length": 4, "height": 6, "width": 4},
                         {"length": 5, "height": 4, "width": 5}])
    assert g.placeBoxesSequentially()
    print("")

    print("TEST CASE 8 ##############################")
    h = Container(length=6, width=10, height=10,
                  boxes=[{"length": 5, "height": 5, "width": 5}, {"length": 4, "height": 6, "width": 4},
                         {"length": 5, "height": 4, "width": 5}, {"length": 4, "height": 4, "width": 4},
                         {"length": 3, "height": 3, "width": 3}])
    result = h.placeBoxesSequentially()
    assert not result
    print("")


    print("TEST CASE 9 ##############################")
    start = time.time()
    i = Container(length=7, width=10, height=10,
                  boxes=[{"length": 5, "height": 5, "width": 5}, {"length": 4, "height": 6, "width": 4},
                         {"length": 5, "height": 4, "width": 5}, {"length": 4, "height": 4, "width": 4},
                         {"length": 3, "height": 3, "width": 3}])
    result = i.placeBoxesSequentially()
    end = time.time()
    print("Took %s seconds" % (end - start))
    assert result
    print("")

    print("TEST CASE 10 ##############################")
    start = time.time()
    # testing scaling factor of minBoxEdgeSize
    j = Container(length=70, width=100, height=100,
                  boxes=[{"length": 50, "height": 50, "width": 50}, {"length": 40, "height": 60, "width": 40},
                         {"length": 50, "height": 40, "width": 50}, {"length": 40, "height": 40, "width": 40},
                         {"length": 30, "height": 30, "width": 30}], spaceOptimizationFactor=1)
    result = j.placeBoxesSequentially()
    end = time.time()
    print("Took %s seconds with 1x" % (end - start))
    assert result
    print("")

    print("TEST CASE 11 ##############################")
    start = time.time()
    # testing scaling factor of minBoxEdgeSize
    k = Container(length=70, width=100, height=100,
                  boxes=[{"length": 50, "height": 50, "width": 50}, {"length": 40, "height": 60, "width": 40},
                         {"length": 50, "height": 40, "width": 50}, {"length": 40, "height": 40, "width": 40},
                         {"length": 30, "height": 30, "width": 30}], spaceOptimizationFactor=5)
    result = k.placeBoxesSequentially()
    end = time.time()
    print("Took %s seconds with 5x" % (end - start))
    assert result
    print("")

    print("TEST CASE 12 ##############################")
    start = time.time()
    # testing scaling factor of minBoxEdgeSize
    l = Container(length=70, width=100, height=100,
                  boxes=[{"length": 50, "height": 50, "width": 50}, {"length": 40, "height": 60, "width": 40},
                         {"length": 50, "height": 40, "width": 50}, {"length": 40, "height": 40, "width": 40},
                         {"length": 30, "height": 30, "width": 30}], spaceOptimizationFactor=10)
    result = l.placeBoxesSequentially()
    end = time.time()
    print("Took %s seconds with 10x" % (end - start))
    assert result
    print("")

    print("TEST CASE 13 ##############################")
    start = time.time()
    # testing deepSearch: Better but slower iterations....
    k = Container(length=70, width=100, height=100,
                  boxes=[{"length": 50, "height": 50, "width": 50}, {"length": 40, "height": 60, "width": 40},
                         {"length": 50, "height": 40, "width": 50}, {"length": 40, "height": 40, "width": 40},
                         {"length": 30, "height": 30, "width": 30}], spaceOptimizationFactor=1, useDeepSearch=True)
    result = k.placeBoxesSequentially()
    end = time.time()
    print("Took %s seconds" % (end - start))
    assert result
    print("")