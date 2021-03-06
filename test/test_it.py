from __future__ import absolute_import, division, print_function, unicode_literals

import random
import unittest
from datetime import datetime

from timezonefinder.timezonefinder import TimezoneFinder
from tzwhere.tzwhere import tzwhere

# number of points to test (in each test, realistic and random ones)
N = 1000

# sets if tzwhere should be used with shapely
SHAPELY = False

# mistakes in these zones dont count as mistakes
excluded_zones_timezonefinder = []
# ['Asia/Srednekolymsk', 'Asia/Chita', 'Europe/Astrakhan', ]
# 'Africa/Johannesburg', "America/Phoenix", 'America/Denver', ]
excluded_zones_tzwhere = []
# 'Asia/Yakutsk', 'Asia/Magadan', 'Europe/Volgograd', ]
# 'Africa/Maseru', "America/Phoenix", 'America/Denver', ]


TEST_LOCATIONS = (
    (35.295953, -89.662186, 'Arlington, TN', 'America/Chicago'),
    (33.58, -85.85, 'Memphis, TN', 'America/Chicago'),
    (61.17, -150.02, 'Anchorage, AK', 'America/Anchorage'),
    (44.12, -123.22, 'Eugene, OR', 'America/Los_Angeles'),
    (42.652647, -73.756371, 'Albany, NY', 'America/New_York'),
    (55.743749, 37.6207923, 'Moscow', 'Europe/Moscow'),
    (34.104255, -118.4055591, 'Los Angeles', 'America/Los_Angeles'),
    (55.743749, 37.6207923, 'Moscow', 'Europe/Moscow'),
    (39.194991, -106.8294024, 'Aspen, Colorado', 'America/Denver'),
    (50.438114, 30.5179595, 'Kiev', 'Europe/Kiev'),
    (12.936873, 77.6909136, 'Jogupalya', 'Asia/Kolkata'),
    (38.889144, -77.0398235, 'Washington DC', 'America/New_York'),
    (59.932490, 30.3164291, 'St Petersburg', 'Europe/Moscow'),
    (50.300624, 127.559166, 'Blagoveshchensk', 'Asia/Yakutsk'),
    (42.439370, -71.0700416, 'Boston', 'America/New_York'),
    (41.84937, -87.6611995, 'Chicago', 'America/Chicago'),
    (28.626873, -81.7584514, 'Orlando', 'America/New_York'),
    (47.610615, -122.3324847, 'Seattle', 'America/Los_Angeles'),
    (51.499990, -0.1353549, 'London', 'Europe/London'),
    (51.256241, -0.8186531, 'Church Crookham', 'Europe/London'),
    (51.292215, -0.8002638, 'Fleet', 'Europe/London'),
    (48.868743, 2.3237586, 'Paris', 'Europe/Paris'),
    (22.158114, 113.5504603, 'Macau', 'Asia/Macau'),
    (56.833123, 60.6097054, 'Russia', 'Asia/Yekaterinburg'),
    (60.887496, 26.6375756, 'Salo', 'Europe/Helsinki'),
    (52.799992, -1.8524408, 'Staffordshire', 'Europe/London'),
    (5.016666, 115.0666667, 'Muara', 'Asia/Brunei'),
    (-41.466666, -72.95, 'Puerto Montt seaport', 'America/Santiago'),
    (34.566666, 33.0333333, 'Akrotiri seaport', 'Asia/Nicosia'),
    (37.466666, 126.6166667, 'Inchon seaport', 'Asia/Seoul'),
    (42.8, 132.8833333, 'Nakhodka seaport', 'Asia/Vladivostok'),
    (50.26, -5.051, 'Truro', 'Europe/London'),

    # test cases for hole handling:
    (41.0702284, 45.0036352, 'Aserbaid. Enklave', 'Asia/Baku'),
    (39.8417402, 70.6020068, 'Tajikistani Enklave', 'Asia/Dushanbe'),
    (47.7024174, 8.6848462, 'Busingen Ger', 'Europe/Busingen'),
    (46.2085101, 6.1246227, 'Genf', 'Europe/Zurich'),
    (-29.391356857138753, 28.50989829115889, 'Lesotho', 'Africa/Maseru'),
    (39.93143377877638, 71.08546583764965, 'usbekish enclave', 'Asia/Tashkent'),
    (40.0736177, 71.0411812, 'usbekish enclave', 'Asia/Tashkent'),
    (35.7396116, -110.15029571, 'Arizona Desert 1', 'America/Denver'),
    (36.4091869, -110.7520236, 'Arizona Desert 2', 'America/Phoenix'),
    (36.10230848, -111.1882385, 'Arizona Desert 3', 'America/Phoenix'),

    # Not sure about the right result:
    # (68.3597987,-133.745786, 'America', 'America/Inuvik'),


    (50.26, -9.051, 'Far off Cornwall', None)
)

TEST_LOCATIONS_PROXIMITY = (
    (35.295953, -89.662186, 'Arlington, TN', 'America/Chicago'),
    (33.58, -85.85, 'Memphis, TN', 'America/Chicago'),
    (61.17, -150.02, 'Anchorage, AK', 'America/Anchorage'),
    (40.7271, -73.98, 'Shore Lake Michigan', 'America/New_York'),
)


def random_point():
    # tzwhere does not work for points with more latitude!
    return random.uniform(-180, 180), random.uniform(-84, 84)


def list_of_random_points(length):
    return [random_point() for i in range(length)]


class PackageEqualityTest(unittest.TestCase):
    # do the preparations which have to be made only once

    if SHAPELY:
        print('shapely: ON (tzwhere)')
    else:
        print('shapely: OFF (tzwhere)')

    if TimezoneFinder.using_numba():
        print('Numba: ON (timezonefinder)')
    else:
        print('Numba: OFF (timezonefinder)')

    start_time = datetime.now()
    timezone_finder = TimezoneFinder()
    end_time = datetime.now()
    my_time = end_time - start_time

    print('Starting tz_where. This could take a moment...')

    # integrated start up time test:
    # (when doing this for multiple times things are already cached and therefore produce misleading results)
    start_time = datetime.now()
    tz_where = tzwhere(shapely=SHAPELY)
    end_time = datetime.now()
    his_time = end_time - start_time

    print('\nStartup times:')
    print('tzwhere:', his_time)
    print('timezonefinder:', my_time)
    try:
        print(round(his_time / my_time, 2), 'times faster')
    except TypeError:
        pass
    print('\n\n')

    # create an array of n points where tzwhere finds something (realistic queries)
    print('collecting and storing', N, 'realistic points for the tests...')
    realistic_points = []
    real_ps_results_tzwhere = []
    real_ps_results_certain = []

    ps_for_10percent = int(N / 10)
    percent_done = 0

    i = 0
    while i < N:
        lng, lat = random_point()
        his_result = tz_where.tzNameAt(lat, lng)
        result_certain = timezone_finder.certain_timezone_at(lng, lat)

        # a realistic point is a point where certain_timezone_at() or tzwhere find something
        if his_result is not None or result_certain is not None:
            i += 1
            realistic_points.append((lng, lat))
            if i % ps_for_10percent == 0:
                percent_done += 10
                print(percent_done, '%')

    print("Done.")

    def test_correctness(self):
        print('\nresults timezone_at()')
        template = '{0:20s} | {1:20s} | {2:20s} | {3:2s}'
        no_mistakes_made = True
        print(template.format('LOCATION', 'EXPECTED', 'COMPUTED', '=='))
        print('====================================================================')
        for (lat, lon, loc, expected) in TEST_LOCATIONS:
            computed = self.timezone_finder.timezone_at(lon, lat)

            if computed == expected:
                ok = 'OK'
            else:
                print(lat, lon)
                ok = 'XX'
                no_mistakes_made = False
            print(template.format(loc, str(expected), str(computed), ok))

        assert no_mistakes_made

        print('\ncertain_timezone_at():')
        no_mistakes_made = True
        print(template.format('LOCATION', 'EXPECTED', 'COMPUTED', 'Status'))
        print('====================================================================')
        for (lat, lon, loc, expected) in TEST_LOCATIONS:
            computed = self.timezone_finder.certain_timezone_at(lon, lat)
            if computed == expected:
                ok = 'OK'
            else:
                print(lat, lon)
                ok = 'XX'
                no_mistakes_made = False
            print(template.format(loc, str(expected), str(computed), ok))

        assert no_mistakes_made

        print('\nclosest_timezone_at():')
        no_mistakes_made = True
        print(template.format('LOCATION', 'EXPECTED', 'COMPUTED', 'Status'))
        print('====================================================================')
        for (lat, lon, loc, expected) in TEST_LOCATIONS_PROXIMITY:
            computed = self.timezone_finder.closest_timezone_at(lon, lat)
            if computed == expected:
                ok = 'OK'
            else:
                print(lat, lon)
                ok = 'XX'
                no_mistakes_made = False
            print(template.format(loc, str(expected), str(computed), ok))

        assert no_mistakes_made

    def test_equality(self):
        # Test the equality of the two packages for N realistic and N random points
        def print_equality_test(types_of_points, list_of_points):
            print('\ntesting', N, types_of_points)
            print('MISMATCHES:')
            template = '{0:40s} | {1:20s} | {2:21s} | {3:20s}'
            print(template.format('Point', 'timezone_at()', 'certain_timezone_at()', 'tzwhere'))
            print('=========================================================================')
            mistakes = 0
            for lng, lat in list_of_points:
                his_result = self.tz_where.tzNameAt(lat, lng)
                my_result_certain = self.timezone_finder.certain_timezone_at(lng, lat)
                # test only makes sense if certain_timezone_at() or tzwhere find something
                if his_result is not None or my_result_certain is not None:
                    my_result = self.timezone_finder.timezone_at(lng, lat)
                    if my_result != his_result or my_result_certain != his_result:
                        if his_result in excluded_zones_tzwhere and my_result in excluded_zones_timezonefinder:
                            print(template.format((lat, lng), my_result, my_result_certain,
                                                  his_result), '(not counted, see issue section)')
                        else:
                            mistakes += 1
                            print(template.format(str((lat, lng)), str(my_result), str(my_result_certain),
                                                  str(his_result)))
            print('\nin', N, 'tries', mistakes, 'mismatches were made')
            fail_percentage = mistakes * 100 / (2 * N)
            assert fail_percentage < 5

        print_equality_test('realistic points', self.realistic_points)
        print_equality_test('random points', list_of_random_points(length=N))

    def test_speed(self):
        def check_speed_his_algor(list_of_points):
            start_time = datetime.now()
            for point in list_of_points:
                self.tz_where.tzNameAt(latitude=point[1], longitude=point[0])
            end_time = datetime.now()
            return end_time - start_time

        def check_speed_my_algor(list_of_points):
            start_time = datetime.now()
            for point in list_of_points:
                self.timezone_finder.timezone_at(*point)
            end_time = datetime.now()
            return end_time - start_time

        def print_speed_test(type_of_points, list_of_points):
            my_time = check_speed_my_algor(list_of_points)
            his_time = check_speed_his_algor(list_of_points)
            print('')
            print('\nTIMES for ', N, type_of_points)
            print('tzwhere:', his_time)
            print('timezonefinder:', my_time)
            try:
                print(round(his_time / my_time, 2), 'times faster')
            except TypeError:
                pass
                # assert his_time > my_time

        print('\n\n')
        if SHAPELY:
            print('shapely: ON (tzwhere)')
        else:
            print('shapely: OFF (tzwhere)')
        if TimezoneFinder.using_numba():
            print('Numba: ON (timezonefinder)')
        else:
            print('Numba: OFF (timezonefinder)')
        print_speed_test('realistic points', self.realistic_points)
        print_speed_test('random points', list_of_random_points(length=N))
