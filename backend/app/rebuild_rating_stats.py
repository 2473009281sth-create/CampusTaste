import argparse
import logging

from sqlmodel import Session

from app.core.db import engine
from app.services.rating_stats import validate_or_rebuild_rating_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="校验或重建菜品评分聚合")
    parser.add_argument(
        "--repair", action="store_true", help="将不一致的聚合修复为评价表计算结果"
    )
    args = parser.parse_args()
    with Session(engine) as session:
        mismatches = validate_or_rebuild_rating_stats(session, repair=args.repair)
    for mismatch in mismatches:
        logger.warning("评分聚合不一致: %s", mismatch)
    if mismatches and not args.repair:
        logger.error("发现 %d 个不一致；使用 --repair 修复", len(mismatches))
        return 1
    logger.info("评分聚合校验完成，不一致数量: %d", len(mismatches))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
