#include <iostream>

using namespace std;

int main()
{
	int count;
	cudaGetDeviceCount(&count);
	cudaDeviceProp prop;

	for (int i = 0; i < count ; ++i )
	{
		cudaGetDeviceProperties(&prop, i);
		cout << "Device : " << prop.name << endl;
		cout << "Compute Capability " << prop.major << " : "
				<< prop.minor << endl ;
		cout << "Grid Dimension " << prop.maxGridSize[0] << " x "
			 << prop.maxGridSize[1] << " x "<< prop.maxGridSize[2] << endl;

		cout << "Block Dimension " << prop.maxThreadsDim[0] << " x "
			 << prop.maxThreadsDim[1] << " x "<< prop.maxThreadsDim[2] << endl;
	}

	return 0;
}
