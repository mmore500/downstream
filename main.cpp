#include <cassert>
#include <csignal>
#include <cstdint>
#include <iostream>
#include <string>
#include <string_view>

#include "impl/_dispatch_assign_storage_site.hpp"
#include "include/downstream/_auxlib/can_type_fit_value.hpp"

template <template <typename> typename Algo>
struct HostEvalAssignStorageSite {
    void operator()(std::uint64_t S, std::uint64_t T, std::uint64_t Smx) {
        const bool has_capacity = Algo<std::uint64_t>::has_ingest_capacity(S, T);
        assert(!downstream::_auxlib::can_type_fit_value<std::uint8_t>(S)
            || !downstream::_auxlib::can_type_fit_value<std::uint8_t>(T)
            || (Algo<std::uint8_t>::has_ingest_capacity(S, T) == has_capacity));
        assert(!downstream::_auxlib::can_type_fit_value<std::uint16_t>(S)
            || !downstream::_auxlib::can_type_fit_value<std::uint16_t>(T)
            || (Algo<std::uint16_t>::has_ingest_capacity(S, T) == has_capacity));
        assert(!downstream::_auxlib::can_type_fit_value<std::uint32_t>(S)
            || !downstream::_auxlib::can_type_fit_value<std::uint32_t>(T)
            || (Algo<std::uint32_t>::has_ingest_capacity(S, T) == has_capacity));

        if (has_capacity) {
            const auto maybe_site = Algo<std::uint64_t>::assign_storage_site(S, T);
            assert(!downstream::_auxlib::can_type_fit_value<std::uint8_t>(S * Smx)
                || !downstream::_auxlib::can_type_fit_value<std::uint8_t>(T)
                || (Algo<std::uint8_t>::assign_storage_site(S, T) == maybe_site));
            assert(!downstream::_auxlib::can_type_fit_value<std::uint16_t>(S * Smx)
                || !downstream::_auxlib::can_type_fit_value<std::uint16_t>(T)
                || (Algo<std::uint16_t>::assign_storage_site(S, T) == maybe_site));
            assert(!downstream::_auxlib::can_type_fit_value<std::uint32_t>(S * Smx)
                || !downstream::_auxlib::can_type_fit_value<std::uint32_t>(T)
                || (Algo<std::uint32_t>::assign_storage_site(S, T) == maybe_site));

            std::cout << (maybe_site ? std::to_string(*maybe_site) : "None");
            std::cout << '\n';
        } else {
            std::cout << '\n';
        }
    }
};

int main(int argc, char* argv[]) {
    std::signal(SIGPIPE, SIG_IGN); // Ignore broken pipe signals
    std::ios_base::sync_with_stdio(false); // Disable sync w/ C stdio for perf

    std::string_view target_name(argv[1]);
    return downstream::dispatch_assign_storage_site<
        HostEvalAssignStorageSite>(target_name);
}
