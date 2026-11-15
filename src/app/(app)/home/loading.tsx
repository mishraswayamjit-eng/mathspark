import HomeSkeleton from '@/components/home/HomeSkeleton';

// The same skeleton component is used everywhere the Home screen waits,
// so there is exactly one loading layout.
export default function HomeLoading() {
  return <HomeSkeleton />;
}
