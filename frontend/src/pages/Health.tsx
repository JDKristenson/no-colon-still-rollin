import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const API_URL = '/api';

// Available tags for stool tracking
const AVAILABLE_TAGS = [
  'Brown', 'Dark Brown', 'Black', 'Green', 'Yellow', 'Red',
  'Hard', 'Soft', 'Loose', 'Watery', 'Mucus', 'Blood',
  'Undigested Food', 'Normal', 'Urgent', 'Painful'
];

export default function Health() {
  const queryClient = useQueryClient();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [notes, setNotes] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [uploading, setUploading] = useState(false);
  const [selectedPhoto, setSelectedPhoto] = useState<any>(null);
  const [showArchived, setShowArchived] = useState(false);
  const [editingTags, setEditingTags] = useState<string[]>([]);

  // Fetch health photos (filtered by archived status)
  const { data: photos } = useQuery({
    queryKey: ['health-photos', showArchived],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/health-photos/list-filtered?user_id=1&archived=${showArchived}`);
      if (!res.ok) throw new Error('Failed to fetch photos');
      return res.json();
    },
  });

  // Fetch stats
  const { data: stats } = useQuery({
    queryKey: ['health-photos-stats'],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/health-photos/stats?user_id=1`);
      if (!res.ok) throw new Error('Failed to fetch stats');
      return res.json();
    },
  });

  // Upload mutation
  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('user_id', '1');
      formData.append('date', date);
      formData.append('photo_type', 'health');
      formData.append('notes', notes);

      const res = await fetch(`${API_URL}/health-photos/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('Upload failed');

      // Reset form
      setSelectedFile(null);
      setNotes('');
      setDate(new Date().toISOString().split('T')[0]);

      // Refresh photos
      queryClient.invalidateQueries({ queryKey: ['health-photos'] });
      queryClient.invalidateQueries({ queryKey: ['health-photos-stats'] });

      alert('Photo uploaded successfully!');
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload photo');
    } finally {
      setUploading(false);
    }
  };

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: async (photoId: number) => {
      const res = await fetch(`${API_URL}/health-photos/${photoId}`, {
        method: 'DELETE',
      });
      if (!res.ok) throw new Error('Delete failed');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['health-photos'] });
      queryClient.invalidateQueries({ queryKey: ['health-photos-stats'] });
      setSelectedPhoto(null);
    },
  });

  // Update tags mutation
  const updateTagsMutation = useMutation({
    mutationFn: async ({ photoId, tags }: { photoId: number; tags: string[] }) => {
      const res = await fetch(`${API_URL}/health-photos/${photoId}/tags`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tags),
      });
      if (!res.ok) throw new Error('Failed to update tags');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['health-photos'] });
      if (selectedPhoto) {
        setSelectedPhoto({ ...selectedPhoto, tags: editingTags });
      }
    },
  });

  // Archive mutation
  const archiveMutation = useMutation({
    mutationFn: async ({ photoId, archived }: { photoId: number; archived: boolean }) => {
      const res = await fetch(`${API_URL}/health-photos/${photoId}/archive?archived=${archived}`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Failed to archive photo');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['health-photos'] });
      setSelectedPhoto(null);
    },
  });

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleSaveTags = () => {
    if (selectedPhoto) {
      updateTagsMutation.mutate({ photoId: selectedPhoto.id, tags: editingTags });
    }
  };

  const handleArchive = () => {
    if (selectedPhoto) {
      archiveMutation.mutate({ photoId: selectedPhoto.id, archived: !selectedPhoto.archived });
    }
  };

  const toggleTag = (tag: string) => {
    if (editingTags.includes(tag)) {
      setEditingTags(editingTags.filter(t => t !== tag));
    } else {
      setEditingTags([...editingTags, tag]);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Health Tracking</h1>
        <p className="mt-1 text-sm text-gray-500">
          Keep your health photos organized and accessible for your medical team
        </p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="text-center">
                <dt className="text-sm font-medium text-gray-500">Total Photos</dt>
                <dd className="text-3xl font-semibold text-primary">{stats.total_photos}</dd>
              </div>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="text-center">
                <dt className="text-sm font-medium text-gray-500">Most Recent</dt>
                <dd className="text-lg font-semibold text-secondary">
                  {stats.most_recent_date
                    ? new Date(stats.most_recent_date).toLocaleDateString()
                    : 'No photos yet'}
                </dd>
              </div>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="text-center">
                <dt className="text-sm font-medium text-gray-500">Categories</dt>
                <dd className="text-3xl font-semibold text-keto">{stats.by_type?.length || 0}</dd>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Upload Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload New Photo</h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="photo" className="block text-sm font-medium text-gray-700 mb-2">
              Select Photo
            </label>
            <input
              type="file"
              id="photo"
              accept="image/*"
              onChange={handleFileSelect}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-blue-700"
            />
            {selectedFile && (
              <p className="mt-2 text-sm text-gray-600">Selected: {selectedFile.name}</p>
            )}
          </div>

          <div>
            <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-2">
              Date
            </label>
            <input
              type="date"
              id="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
            />
          </div>

          <div>
            <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-2">
              Notes (Optional)
            </label>
            <textarea
              id="notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              placeholder="Add any notes about this photo..."
              className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
            />
          </div>

          <button
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            className="w-full px-4 py-3 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-300 font-medium"
          >
            {uploading ? 'Uploading...' : 'Upload Photo'}
          </button>
        </div>
      </div>

      {/* Photo Gallery */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            Your Photos ({photos?.length || 0})
          </h2>
          <button
            onClick={() => setShowArchived(!showArchived)}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              showArchived
                ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                : 'bg-primary text-white hover:bg-blue-700'
            }`}
          >
            {showArchived ? 'Show Active' : 'Show Archived'}
          </button>
        </div>
        {photos && photos.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {photos.map((photo: any) => (
              <div
                key={photo.id}
                className="group relative aspect-square bg-gray-100 rounded-lg overflow-hidden cursor-pointer hover:ring-2 hover:ring-primary"
                onClick={() => {
                  setSelectedPhoto(photo);
                  setEditingTags(photo.tags || []);
                }}
              >
                <img
                  src={`${API_URL}${photo.url}`}
                  alt={`Health photo from ${new Date(photo.date).toLocaleDateString()}`}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/0 to-black/0 flex flex-col justify-end p-2">
                  <p className="text-white text-xs mb-1">
                    {new Date(photo.date).toLocaleDateString()}
                  </p>
                  {photo.tags && photo.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {photo.tags.slice(0, 3).map((tag: string) => (
                        <span
                          key={tag}
                          className="text-[10px] px-1.5 py-0.5 bg-primary text-white rounded"
                        >
                          {tag}
                        </span>
                      ))}
                      {photo.tags.length > 3 && (
                        <span className="text-[10px] px-1.5 py-0.5 bg-gray-600 text-white rounded">
                          +{photo.tags.length - 3}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">No photos uploaded yet.</p>
            <p className="text-sm text-gray-400 mt-2">
              Upload your first photo using the form above.
            </p>
          </div>
        )}
      </div>

      {/* Photo Details Modal */}
      {selectedPhoto && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Photo Details</h2>
                <p className="text-sm text-gray-500">
                  {new Date(selectedPhoto.date).toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={() => setSelectedPhoto(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-4">
              <img
                src={`${API_URL}${selectedPhoto.url}`}
                alt={`Health photo from ${new Date(selectedPhoto.date).toLocaleDateString()}`}
                className="w-full rounded-lg"
              />

              {/* Tags Editor */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Tags</h3>
                <div className="flex flex-wrap gap-2 mb-2">
                  {AVAILABLE_TAGS.map((tag) => (
                    <button
                      key={tag}
                      onClick={() => toggleTag(tag)}
                      className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                        editingTags.includes(tag)
                          ? 'bg-primary text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
                <button
                  onClick={handleSaveTags}
                  disabled={updateTagsMutation.isPending}
                  className="w-full px-4 py-2 bg-secondary text-white rounded-md hover:bg-green-700 transition-colors disabled:bg-gray-300"
                >
                  {updateTagsMutation.isPending ? 'Saving...' : 'Save Tags'}
                </button>
              </div>

              {selectedPhoto.notes && (
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">Notes</h3>
                  <p className="text-gray-700">{selectedPhoto.notes}</p>
                </div>
              )}

              <div className="flex gap-3">
                <a
                  href={`${API_URL}${selectedPhoto.url}`}
                  download
                  className="flex-1 px-4 py-2 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors text-center"
                >
                  Download
                </a>
                <button
                  onClick={handleArchive}
                  disabled={archiveMutation.isPending}
                  className="flex-1 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
                >
                  {archiveMutation.isPending
                    ? 'Processing...'
                    : selectedPhoto.archived
                    ? 'Unarchive'
                    : 'Archive'}
                </button>
                <button
                  onClick={() => {
                    if (confirm('Are you sure you want to delete this photo?')) {
                      deleteMutation.mutate(selectedPhoto.id);
                    }
                  }}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
                  disabled={deleteMutation.isPending}
                >
                  {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
