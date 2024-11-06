use std::sync::atomic::AtomicU32;

use chroma_blockstore::{provider::BlockfileProvider, test_arrow_blockfile_provider};
use chroma_types::{test_segment, Chunk, LogRecord, OperationRecord, Segment, SegmentScope};
use indicatif::ProgressIterator;

use crate::log::test::LogGenerator;

use super::{
    metadata_segment::MetadataSegmentWriter, record_segment::RecordSegmentWriter, LogMaterializer,
    SegmentFlusher, SegmentWriter,
};

pub struct TestSegment {
    pub blockfile_provider: BlockfileProvider,
    pub metadata: Segment,
    pub record: Segment,
}

impl TestSegment {
    // WARN: The size of the log chunk should not be too large
    async fn compact_log(&mut self, logs: Chunk<LogRecord>, offset: usize) {
        let materializer =
            LogMaterializer::new(None, logs, Some(AtomicU32::new(offset as u32).into()));
        let materialized_logs = materializer
            .materialize()
            .await
            .expect("Should be able to materialize log.");

        let mut metadata_writer =
            MetadataSegmentWriter::from_segment(&self.metadata, &self.blockfile_provider)
                .await
                .expect("Should be able to initialize metadata writer.");
        metadata_writer
            .apply_materialized_log_chunk(materialized_logs.clone())
            .await
            .expect("Should be able to apply materialized logs.");
        metadata_writer
            .write_to_blockfiles()
            .await
            .expect("Should be able to write to blockfile.");
        self.metadata.file_path = metadata_writer
            .commit()
            .await
            .expect("Should be able to commit metadata.")
            .flush()
            .await
            .expect("Should be able to flush metadata.");

        let record_writer =
            RecordSegmentWriter::from_segment(&self.record, &self.blockfile_provider)
                .await
                .expect("Should be able to initiaize record writer.");
        record_writer
            .apply_materialized_log_chunk(materialized_logs)
            .await
            .expect("Should be able to apply materialized log.");

        self.record.file_path = record_writer
            .commit()
            .await
            .expect("Should be able to commit metadata.")
            .flush()
            .await
            .expect("Should be able to flush metadata.");
    }

    pub async fn populate_with_generator<G>(&mut self, size: usize, generator: &LogGenerator<G>)
    where
        G: Fn(usize) -> OperationRecord,
    {
        let ids: Vec<_> = (1..=size).collect();
        for chunk in ids.chunks(100).progress() {
            self.compact_log(
                generator.generate_chunk(chunk.iter().copied()),
                chunk
                    .first()
                    .copied()
                    .expect("The chunk of offset ids to generate should not be empty.")
                    - 1,
            )
            .await;
        }
    }
}

impl Default for TestSegment {
    fn default() -> Self {
        Self {
            blockfile_provider: test_arrow_blockfile_provider(),
            metadata: test_segment(SegmentScope::METADATA),
            record: test_segment(SegmentScope::RECORD),
        }
    }
}
