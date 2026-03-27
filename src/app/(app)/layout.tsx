import BottomNav from '@/components/BottomNav';
import ServiceWorkerRegistrar from '@/components/ServiceWorkerRegistrar';
import AddToHomeScreen from '@/components/AddToHomeScreen';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <main className="bg-white max-w-lg mx-auto min-h-screen">
        {children}
      </main>
      <BottomNav />
      <AddToHomeScreen />
      <ServiceWorkerRegistrar />
    </>
  );
}
