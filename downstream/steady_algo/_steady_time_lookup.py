import typing


def steady_time_lookup(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Returns
    -------
    typing.Optional[int]
        Ingest time, if any.
    """
    if T < S - 1:  # Patch for before buffer is filled...
        yield from (v if v < T else None for v in steady_lookup_impl(S, S - 1))
    else:  # ... assume buffer has been filled
        yield from steady_lookup_impl(S, T)

    yield None  # Last site is never filled


def steady_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `steady_time_lookup`."""
    assert T >= S - 1  # T <= S redirected to T = S - 1 by steady_time_lookup
    s = S.bit_length() - 1
    t = (T + 1).bit_length() - s  # Current epoch

    b = 0  # Bunch physical index (left-to right)
    m_b__ = 1  # Countdown on segments traversed within bunch
    b_star = True  # Have traversed all segments in bunch?
    k_m__ = s  # Countdown on sites traversed within segment
    h_ = None  # Candidate hanoi value__

    for k in range(S - 1):  # Iterate over buffer sites, except unused last one
        # Calculate info about current segment...
        w = s - b  # Number of sites in current segment (i.e., segment size)
        m = (1 << b) - m_b__  # Calc left-to-right index of current segment
        h_max = t + w - 1  # Max possible hanoi value in segment during epoch

        # Calculate candidate hanoi value...
        _h0, h_ = h_, h_max - (h_max + k_m__) % w
        assert (_h0 == h_) or b_star  # Can skip h calc if b_star is False...
        del _h0  # ... i.e., skip calc within each bunch [[see below]]

        # Decode ingest time of assigned h.v. from segment index g, ...
        # ... i.e., how many instances of that h.v. seen before
        T_bar_k_ = ((2 * m + 1) << h_) - 1  # Guess ingest time
        epsilon_h = (T_bar_k_ >= T) * w  # Correction on h.v. if not yet seen
        h = h_ - epsilon_h  # Corrected true resident h.v.
        T_bar_k = ((2 * m + 1) << h) - 1  # True ingest time
        yield T_bar_k

        # Update within-segment state for next site...
        k_m__ = (k_m__ or w) - 1  # Bump to next site within segment

        # Update h for next site...
        # ... only needed if not calculating h fresh every iter [[see above]]
        h_ += 1 - (h_ >= h_max) * w

        # Update within-bunch state for next site...
        m_b__ -= not k_m__  # Bump to next segment within bunch
        b_star = not (m_b__ or k_m__)  # Should bump to next bunch?
        b += b_star  # Do bump to next bunch, if any
        # Set within-bunch segment countdown, if bumping to next bunch
        m_b__ = m_b__ or (1 << (b - 1))
