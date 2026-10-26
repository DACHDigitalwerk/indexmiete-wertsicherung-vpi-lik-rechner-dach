import argparse, json
from dataclasses import asdict
from .calculator import IndexRentInput, calculate_index_rent

def main() -> None:
    p = argparse.ArgumentParser(description="DACH Indexmiete & Wertsicherung Rechner 2026")
    p.add_argument("--mode", default="DE_WOHN", choices=["DE_WOHN", "DE_GEW", "AT_VPI", "CH_LIK"])
    p.add_argument("--rent", type=float, default=1450.0)
    p.add_argument("--old-idx", type=float, default=114.2)
    p.add_argument("--new-idx", type=float, default=121.6)
    args = p.parse_args()
    res = calculate_index_rent(IndexRentInput(mode=args.mode, current_net_rent=args.rent, index_old=args.old_idx, index_new=args.new_idx))
    print(json.dumps(asdict(res), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
