import functools
from typing import Generator, Tuple

BASE = 10

_nws_part_cache = {}


def nws_part(s: int, k: int, p: int) -> int:
	"""Count numbers with sum `s` among [k*10^p .. (k+1)*10^p)."""
	# Simple cases.
	# Will not be cached.
	if s < k:
		return 0
	elif p == 0 and s == k:
		return 1
	# Next two are not necessary and can be commented.
	elif p == 1 and k <= s <= k + BASE - 1:
		return 1
	elif p == 2 and k <= s <= k + 2 * (BASE - 1):
		return BASE - abs(BASE - (s - k + 1))

	if (cached_value := _nws_part_cache.get((s, k, p))) is not None:
		return cached_value

	# Main case.
	mirror_s = 2 * k + (BASE-1) * p - s
	if mirror_s < s:
		res = nws_part(mirror_s, k, p)
	elif k:
		res = nws_part(s - k, 0, p)
	else:
		res = sum(nws_part(s - i, 0, p-1) for i in range(BASE))

	_nws_part_cache[(s, k, p)] = res
	return res


@functools.lru_cache(1024)
def nws(s: int, n: int) -> int:
	"""Count numbers with digits sum `s` among [1 .. n]."""
	ndigits = digits(n)

	s_left = sum(ndigits)
	res = int(s == s_left)
	for p, d in enumerate(ndigits):
		s_left -= d
		res += sum(nws_part(s - s_left, k, p) for k in range(d))

	return res


@functools.lru_cache(1024)
def digits(n: int) -> Tuple[int]:
	if not isinstance(n, int):
		raise TypeError("n must be int")
	if n < 0:
		raise ValueError("n must be non-negative")

	if n == 0:
		return 0,

	return tuple(_digits(n))


def _digits(n: int) -> Generator[int, None, None]:
	while n:
		n, r = divmod(n, BASE)
		yield r


@functools.lru_cache(1024)
def digsum(n: int) -> int:
	return sum(digits(n))


def cnt_fixed_points(n: int) -> int:
	# nws_sum[s] is number of all numbers from [1, n] with digits sum <= s.
	# nws_sum[0] is exception: it is sentinel value.
	nws_sum = [0, nws(1, n)]
	# Constraint max sum to check.
	oversum = 2
	while nws_sum[-1] != nws_sum[-2]:
		nws_sum.append(nws_sum[-1] + nws(oversum, n))
		oversum += 1

	res = 1  # 1 is fixed point, let's count it.
	for s in range(2, oversum):
		# Check if there is fixed point for sum `s`.
		qmax = nws_sum[s]
		fq = qmax - nws(s, qmax) - nws_sum[s-1]

		if fq == 0 and digsum(qmax) == s:
			res += 1
			continue

		if fq <= 0:
			continue

		qmin = nws_sum[s-1] + 1
		fq = 1 - nws(s, qmin)
		# Hope that fmin always <= 0.
		if fq == 0 and (digsum(qmin) == s or digsum(qmin+1) == s):
			res += 1
			continue

		while qmin + 1 != qmax:
			qmid = (qmin + qmax) >> 1
			fq = qmid - nws(s, qmid) - nws_sum[s-1]

			if fq < 0:
				qmin = qmid
			elif fq > 0:
				qmax = qmid
			else:
				if digsum(qmid) == s or digsum(qmid+1) == s and qmid < qmax:
					res += 1
				break

	return res


def main():
	n = int(input())
	fixed_points = cnt_fixed_points(n)
	print(fixed_points)


if __name__ == "__main__":
	main()
